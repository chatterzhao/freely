---
issue_id: I-20260627T062554Z-A
issue_path: docs/issues/I-20260627T062554Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260627T062554Z-A
- decision: 2007→799 行重写，三类分叉替代 8 source_family
- why_this: 旧 scan 分类混乱、误报严重、无缓存
- alternatives_considered: 渐进修改旧 scan（改动面太大，不如重写）
- boundary_non_goals: 不实现 milestone 一致性检查（后续版本）
- residual_risk: Cat 3 依赖 a2a_tasks agent_id 改编号完成
