# Tasks: 测试证据有显式写入命令，守护进程不再冒充测试结果
- issue_id: I-20261107T120208Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261107T120208Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核写入点/读取点/命令面三处证据（`_update_test_gate` 两处调用、门禁只排除 `not_tested`、`freely help` 无入口）。
- [x] T2: 写 AT-001（6 静态 + 14 行为），基线快照确认 RED `5 ok / 15 failed`。
- [x] T3: `_test_gate_file` + `_test_gate_write` 单一写入点（原子替换）。
- [x] T4: `cmd_test_gate_record`（worktree 校验 / status 枚举 / commit 校验 / rc=2 拒绝）+ dispatcher + usage。
- [x] T5: 删除 `_update_test_gate` 与 `cmd_start`/`cmd_stop` 的调用。
- [x] T6: 跑 GREEN `20 ok / 0 failed`、7 个相关回归基线对比全 MATCH。
- [x] T7: 自举：用新命令给本轮 test 工位记录 `completed` 并通过 `pr-create-guarded` 门禁。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
