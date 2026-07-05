# Implementation Decision Note: A2A Unified Data Flow

- issue_id: I-20260617T063755Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: 将 a2a_task.py 6 个方法从 _db_rpc 迁移到 A2A Server，启用 SSE 流式推送
- why_this: 011030Z Phase A 架构规定所有操作应通过 A2A Server（内存权威），_db_rpc 直连 SQLite 是当时未完成的妥协
- alternatives_considered: (A) 保留 _db_rpc 双路径 — 否决：数据流不统一持续导致 A2A Server 空转；(B) 完全移除 SQLite — 否决：需要崩溃恢复
- boundary_non_goals: 不改变 db_manager 的 SQLite 实现，只消除 client-side _db_rpc
- residual_risk: SSE 新增代码需 daemon 运行验证；a2a_server.py 的 _db_rpc（SQLiteTaskStore）保持不变
