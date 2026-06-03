---
local_id: raw-20260503-0000
kind: raw
phase_state: absorbed
absorbed_into: I-20260503-0000-A
platform_ids:
  github:
    issue_id: '221'
    url: https://github.com/chatterzhao/freely/issues/221
    synced_at: '2026-05-05T14:20:37Z'
  gitee: {}
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/acp-bridge-crash-resilience/issues/I-20260503-0000-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-03T00:00:00Z'
updated_at: '2026-06-03T13:55:31Z'
intake_id: 20260503-0000-acp-bridge-crash
author: human
channel: chat
session_refs: []
platform_state: closed
---

# ACP Bridge crash resilience — four-layer self-healing fix

## Root cause chain

1. **`acp-bridge.py:241` KeyError**: `msg.get('result','')[:100]` fails when ACP server returns
   a non-string `result` field (e.g. dict). The f-string slice triggers `__getitem__(slice(...))`
   which raises KeyError on dict-like objects.

2. **Reader thread crash doesn't stop bridge**: `_read_stdout` only catches `ValueError/OSError`.
   KeyError escapes, daemon thread dies, but bridge process stays alive holding the socket.
   Bridge is now a zombie — alive but non-functional.

3. **Supervisor cleanup incomplete**: `_stop_acp_bridge` pkill patterns don't always match.
   Old bridge process survives supervisor stop.

4. **No health check on reuse**: `_ensure_acp_bridge_running` only checks `kill -0` (process
   alive) and `-S` (socket exists). A zombie bridge passes both checks and is reused, causing
   all subsequent `session/resume` and `session/new` requests to time out → restart storm.

## Fixes applied

### acp-bridge.py
- Line 251: `str()` wrap prevents KeyError from non-string result values
- Lines 217-231: catch `Exception` in stdout reader; on unexpected error, terminate
  server process and set `running=False`, causing bridge to exit cleanly

### freely (bash)
- Lines 11855-11879: new `_acp_bridge_health_check` function — sends initialize request
  via Unix socket and verifies response within 5s
- Lines 11893-11896: `_ensure_acp_bridge_running` calls health check before reusing
  existing bridge; on failure, removes stale PID/socket and starts fresh

## Deeper findings (round 2)

### session/prompt timeout was wall-clock, not idle-based
The bridge used a single 900s wall-clock timeout for session/prompt. If the AI was
actively working (streaming output, executing tool calls) the timer still counted down.
Fixed: activity-based idle timeout — clock resets every time AI produces output.
Default idle timeout: 300s, absolute safety net: 1800s (env-configurable).

### bypassPermissions not propagated on session/resume
`handle_client` only called `session/set_mode` with `bypassPermissions` after
`session/new`. On `session/resume`, the permission mode was not re-applied.
If the session was created with `default` permissions, resumed cycles would
have tools stuck pending waiting for interactive approval (which can't happen
in daemon mode with `--disallowedTools AskUserQuestion`).
Fixed: `session/set_mode` now called after both `session/new` and `session/resume`.

### server_lock held during wait blocked permission response forwarding
`_send_request` held `server_lock` during the entire wait (up to 900s). When a
permission response arrived from the client, `handle_client` (same thread) tried
to acquire `server_lock` again to forward it to server stdin → non-reentrant
lock deadlock. Permission responses never reached the server.
Fixed: split `stdin_write_lock` from `server_lock`. Request setup uses `server_lock`,
stdin write uses `stdin_write_lock`, and neither is held during the response wait.

### run-acp-prompt.py: defense-in-depth session/set_mode
Added explicit `session/set_mode` call after session creation in `run-acp-prompt.py`
to cover both bridge and direct (subprocess) transport modes.

## Full self-healing chain

```
dispatch crash → reader thread dies → bridge exits (socket cleaned)
                                         ↓
              _ensure_acp_bridge_running: bridge not running → starts fresh
              _ensure_acp_bridge_running: bridge alive but zombie → health check fails → restart
              _ensure_acp_bridge_running: fresh bridge → session/new → set_mode bypassPermissions
              handle_client: session/resume → set_mode bypassPermissions (NEW)
              _send_request: no locks held during wait → permission responses flow freely (NEW)
              _send_request: activity-based timeout → AI keeps working if producing output (NEW)
```
