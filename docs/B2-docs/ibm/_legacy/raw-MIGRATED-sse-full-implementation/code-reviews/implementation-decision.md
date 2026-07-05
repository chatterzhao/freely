# Implementation Decision
- issue_id: I-20260623T100903Z-A
- decision: 采用 5 阶段递进方案，从轮询迁移到 SSE 推送，SSE Watchdog 实现持久连接 + ACP 实时注入
- why_this: A2A 官方协议用 SSE 作为标准通知机制，delivery_status 是手搓的非标准字段，5/6 问题由 SSE 缺失导致
- alternatives_considered: 一次性全切换（无过渡期，风险高）、只保留SSE客户端不废弃delivery_status（增加维护负担）、WebSocket替代SSE（A2A标准路径是SSE）
- boundary_non_goals: 内存优先架构、L0-L3兜底检测、CSV清理、Webhook推送通知
- residual_risk: DB迁移不可逆、SSE连接池泄漏、阶段3后无轮询回退
