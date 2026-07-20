---
candidate_id: C-20260720T004008Z-A
status: promoted
source_raw: raw-20260720T004008Z
created_at: '2026-07-20'
milestone: M-20260720T004008Z-A
---

## C-20260720T004008Z-A: launch-kind跨tool用new

- candidate_format_version: v2
- title: launch-kind跨tool用new
- status: promoted
- decision_reason: daemon日志确认跨tool fork→session-id capture timeout 30s。Routa全用new不做fork
- next_action: merge
- acceptance_criteria: 同tool fork, 跨tool new
- promotion_gate: 代码修改完成
- open_questions: []
- acceptance_reviews: [reviewer: self-review, verdict: pass]
- promoted_issue_id: I-20260720T004008Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T004008Z/issues/I-20260720T004008Z-A.md
- milestone: M-20260720T004008Z-A
- session_refs: []
