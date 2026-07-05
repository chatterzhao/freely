# Candidates
## C-20260618T051709Z-A: pr-merge review gate
- candidate_format_version: v2
- title: Add review gate to pr-merge-guarded
- status: promoted
- decision_reason: Review gate missing, pr-merge allowed unreviewed merges
- next_action: pr-create → pr-review → pr-merge
- promoted_issue_path: docs/issues/I-20260618T051709Z-A/issue.md
- milestone: M-20260618T051709Z-A
- acceptance_criteria: pr-merge blocks if no review or verdict!=pass
- promotion_gate: correct
- open_questions: []
- session_refs: []
