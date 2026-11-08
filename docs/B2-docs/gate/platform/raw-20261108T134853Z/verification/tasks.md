# Tasks: GitHub handler 自动补齐缺失标签
- issue_id: I-20261108T134853Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261108T134853Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真机复现 PARTIAL 与标签缺失，证伪现有 open issue 覆盖。
- [x] T2: 写 AT-001（5 静态 + 9 行为，fake subprocess 驱动真实 handler），基线快照确认 RED `7 ok / 12 failed`。
- [x] T3: `GitHubHandler` 加 `_label_names` / `ensure_github_labels` 与有限重试。
- [x] T4: GREEN `19 ok / 0 failed` + 16 个回归基线对比。
- [x] T5: B1/B2/milestone/review 落盘，按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3 | AT-001 |
| T4, T5 | AT-001 |
