# Candidates
## C-20260618T031437Z-A: wt-close remote branch deletion fix
- candidate_format_version: v2
- title: Fix wt-close SELF_ROOT undefined + silent remote delete failures
- status: promoted
- decision_reason: Two trivial bugs causing remote branches to persist after local wt-close. 9 stale branches found.
- next_action: pr-create → pr-merge
- promoted_issue_path: docs/issues/I-20260618T031437Z-A/issue.md
- milestone: M-20260618T031437Z-A
- acceptance_criteria: wt-close deletes remote branches on all platforms
- promotion_gate: code correct
- open_questions: []
- session_refs: []
