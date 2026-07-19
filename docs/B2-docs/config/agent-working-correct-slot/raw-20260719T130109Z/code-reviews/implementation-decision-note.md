---
issue_id: I-20260719T130109Z-A
issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T130109Z/issues/I-20260719T130109Z-A.md
phase_state: completed
---
- issue_id: I-20260719T130109Z-A
## Implementation Decision Note
- decision: L13331 _worker_slot从AGENT_AI_TOOL改为agent-table-query
- why_this: fork路径写入agent_working.slot=claude而非opencode
- alternatives_considered: 不改→slot永远错
- boundary_non_goals: 不改其他slot解析路径
- residual_risk: 无
