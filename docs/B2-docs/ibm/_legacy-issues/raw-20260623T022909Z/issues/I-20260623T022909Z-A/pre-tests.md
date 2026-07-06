# Pre-tests

## Test 1: Scan runs without import error
1. `python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project /Users/zhaoyu/Downloads/code/my-freely/freely --json`
2. Expected: No `ModuleNotFoundError`, valid JSON output

## Test 2: platform-adapter still callable via direct path
1. `python3 docs/system/workspace/scripts/sync/platform-adapter.py`
2. Expected: Help/usage output (not import error)
