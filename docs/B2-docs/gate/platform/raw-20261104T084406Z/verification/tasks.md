# Tasks: severity 从校验值变成可追溯的一等数据
- issue_id: I-20261104T084406Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261104T084406Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核四处丢弃点，证伪 #4149/#4154/#4166/#4151 覆盖范围。
- [x] T2: 写 AT-001（6 静态 + 14 单元 + 10 行为），develop 基线快照确认 RED `3 ok / 14 failed`。
- [x] T3: 契约层：可选字段、`validate` 双形状、`normalize` 回填。
- [x] T4: adapter + feedback：labels 通道与落盘。
- [x] T5: issue-sync：`_labels` 标签与 `cmd_scan` 稳定排序。
- [x] T6: 跑 GREEN `30 ok / 0 failed` + 14 个回归基线对比全 MATCH。
- [x] T7: 补齐 B1/B2 治理文档与 milestone，按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
