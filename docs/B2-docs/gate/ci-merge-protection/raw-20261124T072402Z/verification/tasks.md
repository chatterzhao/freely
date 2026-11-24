# Tasks: I-20261124T072402Z-A

- owner_issue: I-20261124T072402Z-A

## T1 — RED 测试先行
- 编写 `test-governance-check-doc-alignment.py`，在 develop 基线跑出 RED。
## T2 — 更正 workflow 注释
- 删除错误的第 3 条，补充 in_progress 设计态说明。
## T3 — 接入回归
- 新 AT 接入 `bin/test-all` CORE/CI_CORE。
## T4 — GREEN
- test 工位跑 test-all 全绿，写证据。
## T5 — PR 流程
- pr-create → review → merge → wt-close。
