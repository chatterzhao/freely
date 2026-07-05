# Implementation Decision: A2A-Native Delegation
- issue_id: I-20260617T095105Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: 消除 CSV 中转, Task.message 承载完整委派内容, runtime 从 tasks/list 查询
- why_this: A2A Task.message 就是设计用来承载任务内容的(Routa 同样用法),CSV 是 pre-A2A 遗留
- alternatives_considered: (A) 继续修 CSV — 否决: 路径耦合根因无法消除
- boundary_non_goals: 不改变 ACP session/prompt 机制,不改变 Worker exit 汇报机制
- residual_risk: Manager prompt 需要更新 AI 行为,过渡期需兼容旧 a2a-exit 调用
