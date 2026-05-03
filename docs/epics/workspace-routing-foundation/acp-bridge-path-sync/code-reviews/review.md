# Code Review: ACP Bridge Path Sync

- issue: `I-20260503-0115-A`
- reviewed_by: human (zhaoquan)
- review_date: `2026-05-03T01:15:00Z`

## Implementation Decision Note

The fix synchronizes hash-based socket/pid paths across all four files in the ACP bridge
toolchain. The hash approach (SHA256 first 16 hex chars) is retained from commit `805b6d67`
because it prevents AF_UNIX 104-byte path limit issues on macOS.

The path pattern `.freely/run/acp-bridge-{hash}.*` is used instead of `/tmp/freely-acp-{hash}.*`
to keep files in the project directory for discoverability.

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
