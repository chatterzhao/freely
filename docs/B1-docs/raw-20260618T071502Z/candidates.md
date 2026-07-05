# Candidates

## C-20260618T071502Z-A: pr-merge local merge 替代 gh pr merge

- candidate_format_version: v2
- title: Replace gh pr merge --merge with local git merge --no-ff in pr-merge-guarded
- status: promoted
- decision_reason: gh pr merge --merge --body 是 GitHub API 限制，无法传递 Freely-Merge-Path receipt。唯一可靠方案是 local merge。
- next_action: pr-create → pr-review → pr-merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - do_initial_merge 使用 local git merge --no-ff，不再调用 gh pr merge --merge
  - merge commit 包含 Freely-Merge-Path: pr-merge-guarded receipt
  - attempt_develop_push_followthrough_if_needed 自动推送到所有平台
  - wt-create 平台一致性检查通过
- promotion_gate: code change correct, local merge tested
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: fresh
  - summary: 审查 do_initial_merge 函数替换的正确性和完整性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260618T071502Z-A/issue.md
- milestone: M-20260618T071502Z-A
- session_refs: []
