- issue_id: I-20260714T021808Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/issues/I-20260714T021808Z-A.md

## Implementation Decision Note

- decision: Option C — minimal chain fix. Modify 4 functions: `launch_project_runtime_daemon_or_fail` (accept task_mode), `cmd_daemon_start` (pass task_mode), `start_project_runtime` (accept task_mode), `launch_manager_supervisor` (add listen + fix fallback). Guard 3 AI_MODE references.

- why_this: Fixes all 4 defects with minimal function signature changes. `cmd_daemon_run` already parses --task-mode, just needs to pass it. `launch_project_runtime_daemon_or_fail` already accepts project, just needs $2. Design principle preserved: manual start uses passed value (default wait), watchdog restart reads DB.

- alternatives_considered:
  - Option A: full chain refactor with 4 function signature changes → rejected as over-engineered
  - Option B: DB-only approach → rejected because it violates "manual start does not read DB" design rule

- boundary_non_goals:
  - NOT adding AI_MODE initialization to freely init (separate issue)
  - NOT rewriting the entire task_mode state machine
  - NOT changing listen mode scan behavior (already correct)

- residual_risk:
  - `start_project_runtime` called by worker paths without task_mode — $3 defaults to wait (safe)
  - Python spawn shell quoting must be verified
