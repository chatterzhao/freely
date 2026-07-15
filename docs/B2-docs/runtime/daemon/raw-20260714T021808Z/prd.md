# PRD: task_mode propagation fix
- issue_id: I-20260714T021808Z-A

## Goal
Fix task_mode propagation so that `freely daemon start --task-mode auto` actually starts in auto mode, `listen` mode survives watchdog restarts, and daemon no longer crashes on unguarded AI_MODE references.

## Implementation Plan

### A. task_mode pass-through chain
1. `launch_project_runtime_daemon_or_fail`: accept `$2` task_mode → pass to Python subprocess as `--task-mode`
2. `cmd_daemon_start`: pass `$task_mode` to launcher
3. `start_project_runtime`: accept `$3` task_mode → use in `ensure_task_mode_gate`

### B. Watchdog restart fixes
4. `launch_manager_supervisor`: add `listen` to mode check; change fallback from `auto` to `wait`

### C. AI_MODE guards
5. Three log/echo statements: `${AI_MODE:-none}`

## Dev-Loop Handoff
- All changes in single file: `docs/system/workspace/scripts/runtime/freely`
- 7 lines changed, no new files
- bash -n syntax check sufficient for verification
