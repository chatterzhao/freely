# Implementation Decision
- issue_id: I-20260623T162226Z-A
- decision: 4-tier detector in supervisor main loop A-L042→A-L020
- why_this: SSE/state fixes done but no safety net. Industry standard (Costfuse, Circuit Breaker, AgentFuse)
- alternatives_considered: 修改现有 semantic_loop → 拒绝（Guard 10 盲区难修，不如新建）
- boundary_non_goals: 不替代 semantic_loop，不依赖 AI 自我判断
- residual_risk: L2 依赖 #3386（降级方案已准备）
