# Pre-tests: write_task_mode ordering

## Test 1: ensure_freely_db idempotency
- Call ensure_freely_db twice in sequence
- Verify second call returns immediately (health check passes)
- Command: grep -A5 "ensure_freely_db()" freely → confirm L8099 health check

## Test 2: cmd_start call order
- Verify ensure_freely_db appears before write_task_mode in cmd_start
- Command: grep -A3 "resolve_project_or_fail" freely | grep ensure_freely_db

## Test 3: cmd_daemon_start call order
- Same as Test 2 but for cmd_daemon_start
- Command: grep -A3 "resolve_project_or_fail" freely | tail -5 | grep ensure_freely_db

## Test 4: Syntax check
- bash -n freely → no syntax errors
