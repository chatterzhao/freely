---
issue_id: I-20260711T030122Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260711T030122Z-A
## IDN
- decision: 三文档统一身份优先风格，对齐 agent-roles.toml skill 注册
- why_this: agent 文档是 AI 理解自己职责的唯一入口，结构统一降低 AI 理解成本
- alternatives_considered: 保持旧版修 bug — 治标不治本
- boundary_non_goals: 不修改 skill 定义本身，不修改 agent-roles.toml
- residual_risk: 低 — 纯文档修改，不影响运行时行为
