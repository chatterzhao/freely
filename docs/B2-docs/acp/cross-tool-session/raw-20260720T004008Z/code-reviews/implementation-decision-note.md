---
issue_id: I-20260720T004008Z-A / issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T004008Z/issues/I-20260720T004008Z-A.md / phase_state: completed
---
- issue_id: I-20260720T004008Z-A
## Implementation Decision Note
- decision: launch-kind条件化: 同tool fork / 跨tool new
- why_this: daemon日志确认跨tool fork→session-id capture timeout 30s
- alternatives_considered: Routa全用new→浪费同tool缓存命中
- boundary_non_goals: 不改ACP bridge本身
- residual_risk: 无
