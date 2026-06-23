# Implementation Decision
- issue_id: I-20260623T162243Z-A
- decision: 在 append_task_source_patrol_seed_if_needed 中输出 scan_state
- why_this: scan_state 数据已存在，Manager 看不到。8 行，无风险
- alternatives_considered: 不改 → 拒绝，Manager 需要区分 pending vs working
- boundary_non_goals: 不实现 scan_state 更新（已存在）
- residual_risk: 无
