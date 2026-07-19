---
issue_id: I-20260719T113413Z-A
issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/issues/I-20260719T113413Z-A.md
phase_state: completed
---

- issue_id: I-20260719T113413Z-A
- issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/issues/I-20260719T113413Z-A.md

## Implementation Decision Note
- decision: L13310 slot从AGENT_AI_TOOL(Manager的tool)改为agent-table-query解析Worker的slot; L13110 || true改为|| log_warn
- why_this: agent_working.slot写的是claude(Manager)不是opencode(Worker); worker_id=NULL无感知因为错误被吞
- alternatives_considered: (A)不改—slot永远错; (B)只修slot不修错误处理—下次出问题仍然无感知
- boundary_non_goals: 不改agent-table.toml格式; 不改Python agent_assign逻辑
- residual_risk: 无
