# pre-tests: issue state refactor

## Test 1: TERMINAL_RAW excludes completed
```bash
python3 -c "
from task_lifecycle_scan import TERMINAL_RAW
assert 'completed' not in TERMINAL_RAW
assert 'absorbed' in TERMINAL_RAW
assert 'dropped' in TERMINAL_RAW
print('PASS')
"
```

## Test 2: DONE_STATES uses IBM Framework values
```bash
python3 -c "
from task_lifecycle_scan import DONE_STATES
assert 'done' not in DONE_STATES
assert 'done_ibm' not in DONE_STATES
assert 'done_b2_ibm' in DONE_STATES
assert 'completed' in DONE_STATES
print('PASS')
"
```

## Test 3: scan detects absorbed raw as terminal
```bash
# Create a test raw with status=absorbed and run scan
# Expected: no raw_created stage for absorbed raw
echo "not_applicable: requires existing absorbed raw in test data"
```

## Test 4: migration script runs without errors
```bash
cd /path/to/project && SKIP_PLATFORM_CHECK=1 python3 bin/migrate-issue-phase-state .
echo "exit=$?"
# Expected: 0
```
