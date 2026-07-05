# Tasks: live-status-current-runtime-state-reconciliation-governance

- reconcile `last_supervisor_state` in `live-status` from current project-owned supervisor PID truth
- reconcile `last_ai_state` in `live-status` from current project-owned AI PID truth
- collapse `last_exit_reason: starting` to `none` only when AI is confirmed live
- keep reconciliation read-only and local to the status surface
- extend focused `test-freely-live-status` assertions
