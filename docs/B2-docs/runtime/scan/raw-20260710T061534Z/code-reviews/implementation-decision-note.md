---
issue_id: I-20260710T061534Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260710T061534Z-A
## IDN
- decision: idle monitor checks active session/prompt before shutdown; hygiene removed from hardcoded prompt; workflow skill added to delegation
- why_this: idle monitor 误杀工作中的 AI；hygiene 硬编码吃掉 cycle 时间
- alternatives_considered: 增加 timeout — 不解决误判问题
- boundary_non_goals: 不重排 patrol 流程，不扩展 agent-roles.toml
- residual_risk: 零
