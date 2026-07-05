# Code Review
- issue_id: I-20260513T224509Z-A
## Implementation Decision Note
- decision: add local sup_pid_file and child_pid_file to start_project_runtime
- why_this: unbound variable crash on supervisor cleanup
- residual_risk: None — standard run_dir paths
