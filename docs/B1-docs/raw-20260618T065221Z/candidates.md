# Candidates
## C-20260618T065221Z-A: pr-merge local merge + wt-create consistency check
- candidate_format_version: v2
- title: Replace gh pr merge --merge with local git merge; add platform consistency check to wt-create
- status: promoted
- decision_reason: gh pr merge --merge --body 无效导致 receipt 丢失和平台分叉。Local merge 是唯一可靠方案。
- next_action: B2_IBM → dev → pr-create → pr-review → pr-merge
- acceptance_criteria:
  - pr-merge-guarded 使用 local git merge --no-ff，merge commit 包含 receipt
  - 所有平台收到相同 merge commit
  - wt-create 验证多平台 develop HEAD 一致，不一致时清晰报错
  - git pull 不再被 receipt hook 拦截
- promotion_gate: 2 files modified, local merge tested
- open_questions:
  - gh pr close 是否需要？push 后 GitHub 是否自动检测？
- promoted_issue_path: docs/issues/I-20260618T065221Z-A/issue.md
- milestone: M-20260618T065221Z-A
- session_refs: []
