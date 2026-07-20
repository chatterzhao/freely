---
candidate_id: C-20260720T045011Z-A
status: promoted
source_raw: raw-20260720T045011Z
created_at: '2026-07-20'
milestone: M-20260720T045011Z-A
---

## C-20260720T045011Z-A: session ID capture 支持 ses_ 格式

- candidate_format_version: v2
- title: session ID capture 支持 opencode ses_ 格式
- status: promoted
- decision_reason: is_valid_session_id L4028 已支持 ses_+UUID。capture 函数硬编码 UUID-only 导致 opencode Worker 的 session ID 永远无法被捕获
- next_action: merge → start → Worker session_id 正确记录到 agent_working
- acceptance_criteria:
  - capture_worker_session_id_and_store 接受 ses_ 格式
  - agent_working 正确记录 opencode Worker 的 session_id
- promotion_gate: 一行改动
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: Worker cycle log 确认 ses_ 格式合法，is_valid_session_id 已验证
  - verdict: pass
- promoted_issue_id: I-20260720T045011Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T045011Z/issues/I-20260720T045011Z-A.md
- milestone: M-20260720T045011Z-A
- session_refs: []
