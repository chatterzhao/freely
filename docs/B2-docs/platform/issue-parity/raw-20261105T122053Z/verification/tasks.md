# Tasks: 读失败显式标记，健康路径零变化
- issue_id: I-20261105T122053Z-A
- pre_tests_path: docs/B2-docs/platform/issue-parity/raw-20261105T122053Z/verification/pre-tests.md

## 任务分解

- [x] T1: 实现前评审：核查三处读通道的 `return {}`、模块级聚合层 `_safe`、scan 既有 `__degraded__` 消费者、parity 差异计算；确认「健康路径 107 条结构不变」与「调用方无需改动」的约束。
- [x] T2: 编写 `test-open-list-read-degraded.py`（9 项），在未修改 develop 真源上跑确认 RED；修正 ERROR→FAIL、assertIn 打印整份源码、parity 提示文案触发断言三类夹具问题。
- [x] T3: `PlatformHandler` 新增 `read_health`；GitHub GraphQL / REST、Gitee 读通道记录 ok/error/partial，保留 REST 回退。
- [x] T4: 模块级 `list_open_issue_records()` 显式 try/except、跳过非 dict 记录、失败时附加 `__degraded__`。
- [x] T5: `test-platform-open-parity.py` 降级时 SKIP + 重试提示，绝不基于部分清单报假差异。
- [x] T6: 跑 GREEN；真实双平台读取验证健康路径无标记；13 个回归全 PASS，12 个以未修改 develop HEAD 做基线对比零新增失败。
- [x] T7: 复用 `platform/issue-parity` story，`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T8: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7, T8 | AT-001 |
