# Candidates

## C-20260618T024841Z-A: legacy issue
- candidate_format_version: v2
- title: Fix candidate drift, audit gaps, and raw issue data loss
- status: promoted
- decision_reason: Post-merge review of #2956 found three process/code gaps. All are low-risk documentation + one-line code fixes.
- next_action: B2_IBM → pr-create → pr-merge
- acceptance_criteria:
  - C-20260618T015503Z-A acceptance_criteria matches actual implementation
  - wt-close copies raw issue to develop before deleting worktree (if missing)
- promotion_gate: 2 files changed, logic correct
- open_questions: []
- promoted_issue_path: docs/issues/I-20260618T024841Z-A/issue.md
- milestone: M-20260618T024841Z-A
- session_refs: []
