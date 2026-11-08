# Tasks: create/close 以平台侧发现为身份判定源
- issue_id: I-20261108T092758Z-A
- pre_tests_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261108T092758Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核 R14 现场证据与 `cmd_create`/`cmd_close`/`discover_raw_replicas`/`_resolve_raw_identity` 调用链；证伪 5 个高风险字面方案 + 7 个相邻 open issue 覆盖。
- [x] T2: 写 AT-001（8 静态 + 8 单元 + 12 行为，隔离 mock + develop 基线快照），基线确认 RED 7 ok/13 failed。
- [x] T3: 新增纯模块 `replica_guard.py`；`issue-sync` 加 guard 接线（create 幂等/失败关闭、close 回填 + 终态守卫）。
- [x] T4: 跑 GREEN 28 ok/0 failed + 真机 discover-raw 组合验证 + 6 个相关回归基线对比 0 新增失败。
- [x] T5: 人工四层 TDD review → verdict → governance 门禁 → pr-create/pr-merge → wt-close → 打包 → 更新 goal。
