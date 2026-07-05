# Candidates: write_task_mode before ensure_freely_db ordering fix

## C-20260618T091116Z-A
- title: Fix write_task_mode ordering — ensure DB daemon running first
- status: promoted
- promoted_issue_path: docs/issues/I-20260618T091116Z-A/issue.md
- milestone: M-20260618T091116Z-A
- summary: |
    In cmd_start() and cmd_daemon_start(), write_task_mode() calls
    freely-db-cli to write the task mode into SQLite. However,
    ensure_freely_db() (which starts the DB daemon) is called later in
    start_project_runtime(). If the DB daemon is not already running,
    the write silently fails because write_task_mode uses `|| true`.

    Fix: Insert `ensure_freely_db "$project"` before write_task_mode in
    both functions. ensure_freely_db is idempotent (health-check ping
    at L8099), so calling it early is safe — the second call in
    start_project_runtime becomes a no-op.

### Alternatives considered
- **Move write_task_mode to after start_project_runtime**: Rejected.
  write_task_mode must run before startup_self_heal and lock acquisition
  because task_mode affects startup behavior.
- **Make write_task_mode retry on failure**: Rejected. Adds complexity.
  Starting the DB daemon first is simpler and more correct.

### Verification
- ensure_freely_db is idempotent (L8099: `db.ping` health check → early return)
- No ordering dependency between ensure_freely_db and intervening startup ops
- Fix confirmed safe by code review of the startup call chain
