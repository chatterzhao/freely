---
issue_id: I-20260719T133426Z-A
issue_path: docs/B2-docs/a2a/task-role-required/raw-20260719T133426Z/issues/I-20260719T133426Z-A.md
phase_state: completed
---
- issue_id: I-20260719T133426Z-A
## Implementation Decision Note
- decision: L15641+L15684 --status pending → --status submitted
- why_this: A2A标准状态是submitted, pending是旧名已废弃
- alternatives_considered: 不改→worker永不启动
- boundary_non_goals: 不改a2a_task.py的映射逻辑
- residual_risk: 无
