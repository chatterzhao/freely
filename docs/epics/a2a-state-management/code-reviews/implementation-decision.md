# Implementation Decision
- issue_id: I-20260623T140410Z-A
- decision: 分 C→A→B 三组递进修复。C 组优先（运行时 bug），A0 配合 _restore_tasks 的 A1-A3+B1-B4 统一交付
- why_this: C1(wt-close consumed)是隐蔽的运行时 bug——SQLite 拒绝但错误被吞。A0(stop 改状态)是错误的架构——stop 应只杀进程，_restore_tasks 统一判断重启后的状态
- alternatives_considered: 跳过 B1-B4（环境恢复不通知 Manager）→ 拒绝，Manager 需要知道重启后发生了什么
- boundary_non_goals: TTL 清理、内存优先架构、SSE watchdog 变更
- residual_risk: A0 后重启时 working 任务不再自动 input-required，完全依赖 _restore_tasks 的正确性
