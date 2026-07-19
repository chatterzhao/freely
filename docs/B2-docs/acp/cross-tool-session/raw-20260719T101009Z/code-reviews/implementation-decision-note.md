---
issue_id: I-20260719T101009Z-A
issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/issues/I-20260719T101009Z-A.md
phase_state: completed
---

- issue_id: I-20260719T101009Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/issues/I-20260719T101009Z-A.md

## Implementation Decision Note
- decision: Worker+Reviewer shell路径比较base_tool: 同tool fork(cache hit), 不同tool ensure bridge + session/new
- why_this: fork在同tool间共享ACP session context实现缓存命中; 跨tool无法共享session必须new
- alternatives_considered: (A) 不改—跨tool永远超时; (B) 统一用new—浪费同tool缓存命中
- boundary_non_goals: 不改Python acp_session_connect(已正确处理); 不改ACP bridge本身
- residual_risk: 无
