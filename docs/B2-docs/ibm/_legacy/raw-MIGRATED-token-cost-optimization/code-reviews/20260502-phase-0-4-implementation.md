# Code Review: Token 花费优化 Phase 0-4

- issue_id: I-20260502-0500-C
- review_date: 2026-05-02

## Implementation Decision Note

- decision: 分四个 Phase 实施 token 花费优化。Phase 0 可观测性（[CACHE] stderr + cache_metrics + cache-baseline），Phase 1 loop 模式（--loop），Phase 2 Worker 独立 subprocess（--agent），Phase 3 prompt 稳定性分层 + resume delta，Phase 4 错峰调度（max 2 new/cycle）。
- why_this: 当前 Worker 每 turn 重建 session（L1 冷启动），prompt 动态内容破坏 L2 缓存前缀，7-13 并发 session/new 导致 bridge 崩溃。分 Phase 逐步修，每 Phase 独立可测。
- alternatives_considered: 1) session/fork + 共享 bridge（延后，先修崩溃）2) 一次性大重构（风险高，难以调试）
- boundary_non_goals: 不涉及非 ACP 工具、不涉及用户项目的 token 优化
- residual_risk: --delta resume prompt 如果太精简 AI 可能迷失（需端到端验证）；错峰调度 limit=2 可能降低吞吐
