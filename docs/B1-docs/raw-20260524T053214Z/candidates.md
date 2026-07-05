# Candidates

## C-20260524T053214Z-A: legacy issue

- candidate_format_version: v2
- title: ACP session 生命周期接入 tool_switch_events 统一真相源
- status: absorbed
- decision_reason: Freely 运行时死锁——tool_switch_events 已实现但 ACP 路径未接入，导致 session 切换和 bridge 重启后无限循环。4 个集成断点 + 2 个兜底已实现。
- next_action: B2_IBM → I-* → dev-loop → pr-merge-guarded develop
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `select_launch_kind()` ACP 路径调用 `_tool_switch_launch_kind()` 且 cross_tool 强制 fresh
  - `session/new` 成功后 `new_session_id` 写入 `tool_switch_events`
  - `_detect_acp_failure()` 同时检查 bridge log，匹配 "Internal error"
  - `_acp_bridge_has_fatal_error()` 匹配 "Session not found"
  - `run-acp-prompt.py` prompt 模式 session/prompt 失败 → fallback session/new
  - `session-store.py` DB 写入前校验必填字段
- promotion_gate: pre-tests.md 5 项集成验收全部通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 ACP 路径 4 个集成断点的修复完整性和正确性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260524T053214Z-A/issue.md
- milestone: M-20260524T053214Z-A
- session_refs: []
