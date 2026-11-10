# Tasks: guarded PR plan 可诊断 + git 传输超时守卫
- issue_id: I-20261110T052506Z-A
- pre_tests_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真源定位与现场取证（`pr_lifecycle.py:54`、`platform-adapter.py:108-121`、三远端可达性、逐条证伪 6 个相邻 issue）。
- [x] T2: 写 AT-001（4 静态 + 2 对照 + 12 行为），完整 develop 基线确认 RED `6 ok / 12 failed`。
- [x] T3: 实现 `recovery_for_plan()` + error 透传 + `GIT_FETCH_TIMEOUT_SECS` + `run_git()` helper。
- [x] T4: GREEN `18 ok / 0 failed`；64 组状态矩阵 + 9 组聚合零退化对比；8 回归基线对比 0 新增失败。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
