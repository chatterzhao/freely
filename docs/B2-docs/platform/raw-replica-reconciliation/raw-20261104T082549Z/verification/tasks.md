# Tasks: pull 按可用平台回退并复用 sync-debt 记账
- issue_id: I-20261104T082549Z-A
- pre_tests_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261104T082549Z/verification/pre-tests.md

## 任务分解

- [x] T1: 实现前评审：核查 _discover_one 状态语义、raw_reconciliation 的 allow_degraded 决策、既有 sync-debt.py API、wt-create 的 stdout JSON 契约与 _fill_platform_ids 容错；确认 R7/#4195、R11/#4149 不夹带。
- [x] T2: 编写 `test-raw-issue-pull-platform-fallback.py`（12 项），在未修改 develop 真源上跑确认 RED；修正 stderr 污染、TypeError 转 FAIL、隔离仓库缺初始 commit、退出码断言改为行为验证四类夹具问题。
- [x] T3: `pull_raw_issue()` 按 status 过滤 readable / 记录 degraded，显式平台必须可读，三个循环收窄作用域，返回降级清单。
- [x] T4: adapter `pull` CLI 增加 preferred 参数与部分成功 `SystemExit(3)` / 失败 `SystemExit(1)`。
- [x] T5: `bin/raw-issue-pull` 新增 `--platform`，捕获退出码，partial 时复用既有 sync-debt 记账，保持 stdout 单一 JSON。
- [x] T6: `wt-create` 新增 `--source-platform` 并透传；`_pull_raw_issue()` 把 3 视为继续。
- [x] T7: 跑 GREEN 与 12 个回归；11 个以未修改 develop HEAD 做基线对比零新增失败；端到端验证 CLI 退出码 3 / 账本落账 / wt-create 继续。
- [x] T8: 复用 `platform/raw-replica-reconciliation` story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T9: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5, T6 | AT-001 |
| T7, T8, T9 | AT-001 |
