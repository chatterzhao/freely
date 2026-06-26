---
candidate_id: C-20260626T155612Z-A
status: promoted
source_raw: raw-20260626T155612Z
created_at: 2026-06-26
milestone: M-20260626T155612Z-A
---

## C-20260626T155612Z-A: pr-merge-guarded issue-sync before merge

- candidate_format_version: v2
- title: pr-merge-guarded issue-sync before merge + auto-commit
- status: promoted
- decision_reason: issue-sync after merge dirties source worktree, blocking wt-close. Moving before merge + auto-commit mirrors pr-review-guarded.
- next_action: B2_IBM → pr-create-guarded → pr-merge-guarded → wt-close
- revisit_trigger: N/A
- acceptance_criteria:
  - _sync_issues_changed_in_merge runs before git merge
  - After issue-sync, changes auto-committed + pushed in source worktree
  - Diff comparison uses source vs target (pre-merge)
  - Works for fix, feature, feat, hotfix branches
- promotion_gate: 修改完成，通过 review
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 验证 diff 比较逻辑、auto-commit 流程、分支名兼容性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260626T155612Z-A/issue.md
- milestone: M-20260626T155612Z-A
- session_refs: []
