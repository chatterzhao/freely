---
issue_id: I-20260710T002224Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260710T002224Z-A
## Implementation Decision Note
- decision: --skip-ibm → FREELY_SKIP_IBM_GATE 环境变量
- why_this: --skip-ibm 参数不存在于任何命令；FREELY_SKIP_IBM_GATE 是 LAWS.md §304 定义的合法门禁豁免
- alternatives_considered: 实现 --skip-ibm CLI 参数 — 需改多个命令，风险大
- boundary_non_goals: 不新增 CLI 参数
- residual_risk: 零
