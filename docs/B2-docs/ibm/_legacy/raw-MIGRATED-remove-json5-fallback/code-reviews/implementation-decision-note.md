# Implementation Decision Note: remove JSON5 fallback
- issue_id: I-20260624T055231Z-A
- issue_path: docs/issues/I-20260624T055231Z-A/issue.md
- milestone: M-20260624T055231Z-A
## Implementation Decision Note
- decision: 删除 JSON5，去所有回退，只留 TOML
- why_this: #3399 重构不彻底导致 deploy-skills regression
- alternatives_considered: (1) 保留双格式 — 违背重构意图
- boundary_non_goals: 不修改 TOML schema
- residual_risk: 无
