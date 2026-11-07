# Tasks: 两代 receipt 兼容 + 审计链总能跑完
- issue_id: I-20261107T090847Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261107T090847Z/verification/pre-tests.md

## 任务分解

- [x] T1: 证伪评审（上一轮已做）+ 精读 governance-check 控制流，定位 4 类提前退出根因与两代取值统计。
- [x] T2: 编写 `test-governance-receipt-audit`（9 静态 + 6 隔离仓库行为场景），修正探针 helper 抽取边界与静态断言作用域。
- [x] T3: allowlist 同时接受两代合法值并写明历史兼容注释。
- [x] T4: 加固 `check_entry_naming` / `check_no_tbd` / `check_three_loop_reference` / `check_fixed_string` / 空 entries / audit 调用，不削弱任何检查。
- [x] T5: 跑 GREEN；以未修改 develop HEAD 做基线 RED 与 9 个回归对比，0 新增失败；真实 develop HEAD 复验 `PROBE_ERRORS=0` 与汇总行。
- [x] T6: 复用 `gate/governance` story，`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T7: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
| T5, T6, T7 | AT-001 |
