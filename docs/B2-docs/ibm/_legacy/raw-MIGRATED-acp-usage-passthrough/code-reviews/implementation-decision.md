# Implementation Decision
- issue_id: I-20260623T075200Z-A
- decision: prompt_bytes/4 workaround until ACP fixes usage passthrough
- why_this: L0-L3 L2 needs token data. ACP external fix timeline unknown.
- alternatives_considered: 等 ACP 修复 → 拒绝（阻塞 L2）
- boundary_non_goals: 不修改 ACP 项目代码
- residual_risk: bytes/4 是估算（±40%），真实 usage 数据更准确
