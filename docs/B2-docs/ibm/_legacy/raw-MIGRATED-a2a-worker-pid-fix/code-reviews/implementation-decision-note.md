---
issue_id: I-20260627T121248Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260627T121248Z-A
- decision: 补 WT2 遗留的 insert 端和查询端缺口
- why_this: worker_pid 基础设施已存在仅未调用；manager 查询和 worker 查询统一用 startswith
- alternatives_considered: 无（唯一方案）
- boundary_non_goals: 不改 sessions 表
- residual_risk: worker_pid 值需从 fork session 后的 PID 获取
