---
issue_id: I-20260627T084545Z-A
issue_path: docs/issues/I-20260627T084545Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260627T084545Z-A
- decision: 源头改 --role → 具体编号；查询改 LIKE；worker_pid + delivery_status 补全
- why_this: 最小改动，不改 a2a_task.py 的 agent_id=role 逻辑
- alternatives_considered: 新增 --agent-id 单独字段（过度设计）
- boundary_non_goals: 不迁移历史数据
- residual_risk: LIKE 'worker_%' 可能误匹配未来非 worker 的 agent_id
