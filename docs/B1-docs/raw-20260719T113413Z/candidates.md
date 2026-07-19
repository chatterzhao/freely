---
candidate_id: C-20260719T113413Z-A / status: promoted / source_raw: raw-20260719T113413Z
created_at: '2026-07-19' / milestone: M-20260719T113413Z-A
---
## C-20260719T113413Z-A: agent_working slot+agent_id从agent-table解析
- candidate_format_version: v2 / title: agent_working写入时slot和agent_id从agent-table正确解析
- status: promoted / decision_reason: L13110 slot默认claude + 错误吞掉。L13310 slot用AGENT_AI_TOOL(Manager的tool)
- next_action: dev → test → PR
- acceptance_criteria: agent_working.slot=Worker的slot(非claude) / worker_id!=NULL(非空)
- promotion_gate: daemon重启后agent_working写入正确
- open_questions: [] / acceptance_reviews: [reviewer:self-review verdict:pass]
- promoted_issue_id: I-20260719T113413Z-A
- promoted_issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/issues/I-20260719T113413Z-A.md
- milestone: M-20260719T113413Z-A / session_refs: []
