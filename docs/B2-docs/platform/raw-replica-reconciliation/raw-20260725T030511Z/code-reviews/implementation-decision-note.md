---
issue_id: I-20260725T030511Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/issues/I-20260725T030511Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260725T030511Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/issues/I-20260725T030511Z-A.md

## Implementation Decision Note

- decision: 新建纯 `raw_reconciliation` 模块，adapter 只提供 transport records
- why_this: 使所有 lifecycle 共享可测试的 fail-closed 语义，阻断对本地或远端的隐式覆盖
- alternatives_considered: 在 shell 生命周期脚本中逐个比较；拒绝，因为规则会再次漂移
- boundary_non_goals: 本项不执行 resolution 写操作；仅产出其所需的明确差异
- residual_risk: 现有个别平台 handler 的分页能力有限；不能证明完整性时必须返回 degraded
