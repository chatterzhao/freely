# Tasks: 平台写通道失败必报、部分成功可追
- issue_id: I-20261103T132526Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261103T132526Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核 6 处证据点（契约失配、token 未赋值、repo 身份、探测四合一、退出码、文本 grep）。
- [x] T2: 写 AT-001（静态 6 + 行为 16），基线快照确认 RED。
- [x] T3: `bin/issue-sync` 写原语与创建记账重构。
- [x] T4: `platform-adapter.py` 探测报因 + `create-issue` 退出码。
- [x] T5: `runtime/freely` `cmd_feedback` JSON 解析。
- [x] T6: 跑 GREEN、相关回归基线对比、真实仓库只读核验。
- [x] T7: 补齐 B1/B2 治理文档与 milestone，按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
