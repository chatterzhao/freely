# Candidates
## C-20260624T072546Z-A: legacy issue
- candidate_format_version: v2
- title: 修复 wt-create/hook/freely feedback 中的平台硬编码报错
- status: promoted
- decision_reason: 多平台设计下不应假定 GitHub
- next_action: B2_IBM → pr-create → pr-merge → wt-close
- acceptance_criteria:
  - wt-create/hook 报错不出现 "GitHub"/"gh issue create"
  - freely feedback --help 不出现 "GitHub repository"
- promotion_gate: 文件修改完成
- open_questions: []
- acceptance_reviews: [{reviewer: claude, mode: inline, verdict: pass}]
- promoted_issue_path: docs/issues/I-20260624T072546Z-A/issue.md
- milestone: M-20260624T072546Z-A
