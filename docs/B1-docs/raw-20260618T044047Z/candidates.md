# Candidates
## C-20260618T044047Z-A: legacy issue
- candidate_format_version: v2
- title: pr-merge explicit cd + develop cleanliness check
- status: promoted
- decision_reason: pr-merge relies on $PWD, no cd, no develop clean check
- next_action: pr-create → pr-merge
- promoted_issue_path: docs/issues/I-20260618T044047Z-A/issue.md
- milestone: M-20260618T044047Z-A
- acceptance_criteria: pr-merge cd's to PROJECT_ROOT, blocks on dirty develop
- promotion_gate: correct
- open_questions: []
- session_refs: []
