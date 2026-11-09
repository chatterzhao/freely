# Tasks: `runtime/freely` 被 source 时无副作用
- issue_id: I-20261103T132605Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261103T132605Z/verification/pre-tests.md

## 任务分解

- [x] T1: 核对两处顶层 `exit 1`、顶层 `set -euo pipefail`、末尾 `BASH_SOURCE` 守卫、`freely_stop` 的 `|| exit 1`。
- [x] T2: 写 AT-001（2 静态 + 4 行为），基线快照确认 RED `1 ok / 5 failed`。
- [x] T3: 引入 `_FREELY_IS_SOURCED`；sourced 时不改 shell 选项；缺库用 `FREELY_LIB_LOAD_ERROR` + `return 1`（直接执行走 `set -e` 的 `false`）。
- [x] T4: `stop_project_runtime` 改 `|| return 1`；GREEN `6 ok / 0 failed` + 回归。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
