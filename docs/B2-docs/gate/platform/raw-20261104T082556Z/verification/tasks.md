# Tasks: issue-sync 能找到 B2 文档，promote 不再必然失败
- issue_id: I-20261104T082556Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261104T082556Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复现 promote 对 B2 目标的必然失败，列出 5 处同一假设。
- [x] T2: 写 AT-001（5 静态 + 11 行为），基线快照确认 RED `4 ok / 16 failed`。
- [x] T3: 新增 `_issue_file_for` / `_fm_has_key`。
- [x] T4: 5 个命令与 `cmd_promote` 统一走解析器。
- [x] T5: `platform_state` 条件写入。
- [x] T6: 跑 GREEN `16 ok / 0 failed` + 7 个回归基线对比。
- [x] T7: 用修好的 promote 完成本轮自己的 absorb 与平台关闭。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
