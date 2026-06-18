# Candidates
## C-20260618T035220Z-A: merge semantic conflict detection
- candidate_format_version: v2
- title: Post-merge receipt check + actionable hook error
- status: promoted
- decision_reason: Silent receipt loss caused develop deadlock. Two defensive fixes.
- next_action: pr-create → pr-merge
- promoted_issue_path: docs/issues/I-20260618T035220Z-A/issue.md
- milestone: M-20260618T035220Z-A
- acceptance_criteria:
  - pr-merge-guarded detects missing receipt after merge and aborts
  - reference-transaction hook shows commit subject and fix guidance
- promotion_gate: code correct
- open_questions: []
- session_refs: []
