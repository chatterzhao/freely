# Tasks: DB 读写边界收口
- issue_id: I-20261104T075910Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261104T075910Z/verification/pre-tests.md

## 任务分解

- [x] T1: 扫描全工作区 `sqlite3.connect`（20 处，issue 只列 6），按 40 行窗口分类 11 读 / 6 写 / 1 daemon / 1 遗留备份。
- [x] T2: 写 AT-001（5 静态 + 1 守卫 + 5 行为），基线快照确认 RED `5 ok / 6 failed`。
- [x] T3: 新增 `runtime/db_write_gate.py`（reader / writer / write_tx）。
- [x] T4: 11 处只读连接改 `mode=ro`；6 处短写者加 `# db-writer:` 登记。
- [x] T5: 新增 `bin/check-db-writers` + State 契约段（三个辅助 store 登记）；GREEN `11 ok / 0 failed`。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
