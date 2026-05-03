# Code Review: ACP Bridge Path Sync

- issue_id: `I-20260503-0115-A`
- issue_path: `docs/epics/workspace-routing-foundation/acp-bridge-path-sync/issues/I-20260503-0115-A.md`
- reviewed_by: human (zhaoquan)
- review_date: `2026-05-03T01:15:00Z`

## Implementation Decision Note

- decision: Synchronize hash-based socket/pid paths across all four files in the ACP bridge toolchain using `.freely/run/acp-bridge-{hash}.*` pattern
- why_this: Commit `805b6d67` changed acp-bridge.py to use hash-based paths but didn't update the three bash scripts that reference those paths. The resulting path mismatch prevented the ACP bridge from being discovered by clients, blocking all daemon AI launches
- alternatives_considered: (a) Revert acp-bridge.py to non-hash paths — rejected because hash approach is needed for AF_UNIX 104-byte limit on macOS; (b) Use `/tmp/freely-acp-{hash}.*` everywhere — rejected because project-local files are more discoverable and the hash already provides short path protection
- boundary_non_goals: Does not change the hash algorithm, does not modify ACP protocol behavior, does not affect worker bridge sharing
- residual_risk: Minimal. The four files now use consistent paths; if any future changes add new references to bridge socket/pid files, they must use the hash-based functions

## Changes

| File | Change |
|---|---|
| `acp-bridge.py` | Use `.freely/run/acp-bridge-{hash}.*` instead of `/tmp/` |
| `freely` | Add `_acp_bridge_short_hash()`, sync 4 reference points |
| `monitor-ai-acp.sh` | Add `_bridge_short_hash()`, sync `_bridge_pid_file` and `_bridge_socket` |
| `tool-launchers.sh` | Call `_bridge_socket()` instead of hardcoded path |

## Verification

- Daemon start → ACP bridge at correct hash path
- AI session/resume → session/prompt → cycle runs successfully
- AI completes tasks (temp worktree cleanup confirmed)
