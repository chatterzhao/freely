# Implementation Decision: Fix worker_prompts_csv dead loop

- issue_id: I-20260617T090408Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: execute() 中补齐 5 个 Freely 特有字段到 DB insert
- why_this: JSON-RPC tasks/send 的 SDK handler 只处理标准 A2A 字段，Freely 扩展字段需要显式传递
- alternatives_considered: (A) 改 a2a-exit 走 REST 而非 JSON-RPC — 否决：改动面大；(B) 在 metadata 中嵌套传递 — 否决：增加解析复杂度
- boundary_non_goals: 不改变 JSON-RPC 路由，不改变 SDK handler
- residual_risk: 若 Manager 不调 a2a-exit（crash/timeout），filesystem fallback 仍然有效
