# Candidates

## C-20260623T162243Z-A: scan_state 输出到 Manager prompt
- candidate_format_version: v2
- title: scan_state 输出到 Manager prompt + 死 Worker 检测
- status: promoted
- decision_reason: scan_state 数据层已实现，仅需 prompt 输出。8 行改动，无风险。
- next_action: B2_IBM → dev-loop → pr-create
- revisit_trigger: N/A
- acceptance_criteria:
  - Manager prompt 输出 scan_state (pending/working/closed)
  - 输出 scan_state_worktree
  - scan_state=working 无 Worker → 死 Worker 警告
- promotion_gate: 8 行代码改动验证通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: 验证 scan_state 数据层已存在，prompt 输出正确。8 行改动，低风险。
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260623T162243Z-A/issue.md
- milestone: M-20260623T162243Z-A
- session_refs: []
