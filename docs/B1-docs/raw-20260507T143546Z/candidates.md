# Candidates
## C-20260507T143546Z-A: legacy issue
- candidate_format_version: v2
- title: platform pull 时根据 created_at 标准化标题 key
- status: promoted
- decision_reason: best-effort 修正，不阻塞 pull
- next_action: 合并到 develop
- acceptance_criteria: _created_at_to_key 正确转换，_update_issue_title 有异常保护
- promotion_gate: 代码审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 代码路径完整，best-effort 设计合理
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260507T143546Z-A/issue.md
- milestone: M-20260507T143546Z-A
- session_refs: []
