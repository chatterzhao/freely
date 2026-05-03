---
local_id: raw-20260503-acp-bridge-crash
kind: raw
status: absorbed
absorbed_into: I-20260503-0000-A
platform_ids:
  github: {}
  gitee: {}
primary_platform: github
canonical_issue_path: ""
last_synced_comment_at: {}
hash: ""
created_at: "2026-05-03T00:00:00Z"
updated_at: "2026-05-03T00:00:00Z"
intake_id: 20260503-acp-bridge-crash
author: human
channel: chat
session_refs: []
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

## Self-healing chain

```
dispatch crash → reader thread dies → bridge exits (socket cleaned)
                                         ↓
              _ensure_acp_bridge_running: bridge not running → starts fresh
              _ensure_acp_bridge_running: bridge alive but zombie → health check fails → restart
```
