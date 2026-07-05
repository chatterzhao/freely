# PRD: write_task_mode ordering fix

## Problem
write_task_mode() writes to SQLite via freely-db-cli, but was called before
ensure_freely_db() which starts the DB daemon. If the daemon wasn't running,
the write silently failed (`|| true` swallowed the error).

## Fix
Insert `ensure_freely_db "$project"` before write_task_mode in cmd_start()
and cmd_daemon_start().

## Design Decision
- ensure_freely_db is idempotent (L8099 health check)
- No dependency between ensure_freely_db and intervening startup operations
- The later call to ensure_freely_db in start_project_runtime becomes a no-op
