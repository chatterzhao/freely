---
issue_id: I-20260627T121241Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260627T121241Z-A
- decision: 全局路径 + =分割 + 双参数查询
- why_this: agent-id.env 是全局绑定表，不在工位本地
- alternatives_considered: 在工位本地创建 agent-id.env 副本（冗余，增加同步复杂度）
- boundary_non_goals: 不改 sessions 表 schema
- residual_risk: sessions 未来改具体编号后双参数查询仍兼容
