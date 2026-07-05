---
local_id: I-20260616T055035Z-A
kind: linked
phase_state: completed
promoted_from: raw-20260616T055035Z
source_candidate: docs/B1-docs/raw-20260616T055035Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-16T05:50:52Z
updated_at: 2026-06-16T05:50:52Z
intake_id: ""
author: claude
channel: freely-fix-execution
session_refs: []
verification_artifact_dir: docs/B2-docs/a2a-hygiene-after-run/code-reviews
---

# I-20260616T055035Z-A: A2A server hygiene + after-run worker detection for prompt mode

- source_candidate: `docs/B1-docs/raw-20260616T055035Z/candidates.md`
- verification_artifact_dir: `docs/B2-docs/a2a-hygiene-after-run/code-reviews`

## Summary

Three related fixes for A2A server reliability and prompt-mode worker dispatch:

1. **A2A zombie cleanup**: Kill existing A2A processes before starting (via PID file + pkill); store PID in .freely/run/a2a-server.pid; multi-layer cleanup on stop
2. **A2A startup healthcheck**: Replace socket-only check with HTTP GET /tasks health check (10s timeout)
3. **After-run worker detection**: When Manager exits with end_turn, scan worker-prompts/ for new files and trigger delegate_workers

## Changes

File: `docs/system/workspace/scripts/runtime/freely`

### Ensure A2A zombie cleanup on start
- Before launching a2a_server.py, kill any existing processes via temp PID file, cached PID file, and pkill fallback
- Write PID to `.freely/run/a2a-server.pid` for robust stop detection

### HTTP health check on A2A startup (10s timeout)
- After spawning a2a_server.py, wait for socket to appear
- Connect via Unix socket and send GET /tasks HTTP/1.1
- Verify HTTP response received before marking server as ready

### Multi-layer A2A stop
- Always call a2a_server.py --stop (not gated by socket existence)
- Also kill via cached PID with terminate_pid_with_graceful_wait
- pkill fallback for zombie processes

### After-run worker detection for prompt mode
- Detect end_turn via `stop_reason=end_turn` in cycle log
- Scan `.freely/run/worker-prompts/` for files with MTIME >= cycle start
- If found, set exit_contract_action=delegate_workers
- Triggers worker launch before next Manager restart
