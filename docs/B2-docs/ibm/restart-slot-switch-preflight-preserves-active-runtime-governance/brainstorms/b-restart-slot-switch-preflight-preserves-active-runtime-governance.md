# IBM Brainstorm: restart-slot-switch-preflight-preserves-active-runtime-governance

## Goal

Freeze the narrow restart-time contract that bridges the completed startup-lock owner and the completed project-command owner without reopening either parent.

## Decision

1. `freely restart` must run shared codex slot-switch preflight before any stop of the current project runtime.
2. If preflight fails because the shared lock is still active, restart must preserve the current project supervisor and AI child.
3. Helper hardenings that exist only to make that restart contract truthful may stay in this owner:
   - cwd anchoring for relaunch helpers
   - stop-before-launch rechecks
   - atomic session-state replacement
   - finer-grained readiness polling
4. Tests must prove both command ordering and end-to-end runtime preservation.

## Implementation Route

1. Add a restart-specific preflight helper in `runtime/freely` that reuses the existing startup-lock readiness contract.
2. Invoke that helper from `cmd_restart` before `stop_project_runtime`.
3. Harden restart-adjacent helper paths that otherwise make the preserved-runtime contract flaky under supervision churn.
4. Replay focused restart, session, checkpoint, and account-switch regressions that touch the same runtime surfaces.
