# Candidates
## C-20260508T004541Z-A: legacy issue
- candidate_format_version: v2
- title: lead-agent.md skill 引用改为 dual-mode
- status: promoted
- decision_reason: runtime 脚本需兼容 Codex，只改 lead-agent.md
- next_action: 合并到 develop
- revisit_trigger: N/A
- acceptance_criteria: lead-agent.md 使用 dual-mode 引用
- promotion_gate: diff 审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 skill 引用改动，确认 runtime 脚本保留
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260508T004541Z-A/issue.md
- milestone: M-20260508T004541Z-A
- session_refs: []
