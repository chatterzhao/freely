---
issue_id: I-20260625T044836Z-A
issue_path: docs/issues/I-20260625T044836Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T044836Z-A
- issue_path: docs/issues/I-20260625T044836Z-A/issue.md

## Implementation Decision Note

- decision: 在 cmd_batch 收集阶段跳过 platform_state=closed 的 issue
- why_this: 一次本地字段检查即可判断，无需网络请求；200+→~10-20 大幅减少
- alternatives_considered: 平台 API 双重验证 → 慢；不处理 → Manager 浪费 token
- boundary_non_goals: 不处理平台侧 closed + 本地 open 的特殊情况（后续 issue）
- residual_risk: 极少数情况下 platform_state 可能不准（手动修改所致）
