---
local_id: raw-20260616T055035Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2823'
    url: https://github.com/chatterzhao/freely/issues/2823
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T05:50:52Z'
updated_at: '2026-06-16T05:50:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem 1: A2A server startup false timeout
daemon-launch.log: "A2A server start timed out (may be TCP-only)"
But the server IS running and responsive (HTTP 200 OK on socket).
The startup check is too strict or wrong, causing the runtime to believe
A2A is down, which breaks worker dispatch (Manager can't call a2a-exit).

## Problem 2: Zombie A2A processes
5 a2a_server.py processes accumulated from daemon restarts.
Each daemon stop should kill the A2A server but doesn't.
Only the oldest process binds the socket; newer ones fail silently.

## Problem 3: After-run worker detection for prompt mode
When Manager exits with end_turn (prompt mode, no a2a-exit), the worker
prompts written during the cycle are not detected. The after_run
filesystem scan in manager_exit_contract_kind should handle this but
may not be reached before the next Manager cycle starts.

## Fix
### Phase 1: A2A server hygiene
- daemon stop: kill A2A server process (track PID)
- daemon start: wait longer for A2A server, verify with actual HTTP healthcheck
- startup: don't fail on timeout if socket exists and responds

### Phase 2: After-run for prompt mode  
- After end_turn: run filesystem scan for new worker prompts BEFORE
  ensure-manager restarts the Manager
- If new worker prompts found: launch Workers immediately
