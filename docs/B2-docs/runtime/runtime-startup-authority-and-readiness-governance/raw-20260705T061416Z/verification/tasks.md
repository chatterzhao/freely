# Tasks: fix dirty 提示 backtick 命令替换

- issue_id: I-20260705T061416Z-A
- phase_state: completed

## Task List

### A. Implementation (1 task)
- [x] A1. Fix line 21982: remove backtick escaping from log_error message
  - file: `docs/system/workspace/scripts/runtime/freely`
  - change: `\\\`freely-workflow-guarded-execution\\\`` → `freely-workflow-guarded-execution`
  - owner: I-20260705T061416Z-A
  - done: 2026-07-05

### B. Verification (2 tasks)
- [x] B1. Verify syntax: `bash -n docs/system/workspace/scripts/runtime/freely` → PASS
- [x] B2. Verify no backtick: grep check on line 21982 → CLEAN
