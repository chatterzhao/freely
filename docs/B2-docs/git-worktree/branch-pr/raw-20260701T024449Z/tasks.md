# Tasks: _review_guide 修复

- issue_id: I-20260701T024449Z-A

## Task 1: 应用修复
- [x] `bin/pr-review-guarded` L506: `$_review_guide` → `skill:freely-tdd-review`

## Task 2: 验证
- [x] `grep -c '_review_guide' bin/pr-review-guarded` 返回 0
- [x] bash -n 语法检查通过
- [x] `set -euo pipefail` 下不 crash
