- candidate_id: C-20260720T012820Z-A
- status: promoted
- source_raw: raw-20260720T012820Z
- created_at: 2026-07-20
- milestone: M-20260720T012820Z-A

## C-20260720T012820Z-A: cross-tool worker launch-kind new→fresh

- candidate_format_version: v2
- title: cross-tool worker launch-kind new→fresh
- status: promoted
- decision_reason: run-acp-prompt.py --launch-kind 仅接受 fresh/resume/fork/prompt 四种值。cross-tool worker 路径使用 "new" 不在此枚举中，导致 argparse error → worker 立即崩溃。debug log 已确认: "invalid choice: 'new' (choose from fresh, resume, fork, prompt)"。修复方案: new→fresh，一字改动。
- next_action: merge to develop → clear DB → restart freely → observe worker launch
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - cross-tool worker launch 使用 --launch-kind fresh（非 new）
  - worker 启动无 argparse error
  - agent_working 表正确记录 worker 分配
- promotion_gate: 一字改动，语义与 run-acp-prompt.py --help 输出对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 确认 run-acp-prompt.py --help 输出 fresh/resume/fork/prompt 为唯一合法值；debug log 确认 "invalid choice: new" 错误
  - verdict: pass
- promoted_issue_id: I-20260720T012820Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T012820Z/issues/I-20260720T012820Z-A.md
- milestone: M-20260720T012820Z-A
- session_refs: []
