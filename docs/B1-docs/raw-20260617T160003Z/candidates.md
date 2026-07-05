# Candidates

## C-20260617T160003Z-A: legacy issue

- candidate_format_version: v2
- title: Add phase_state guard to wt-close --force so it doesn't overwrite pr-merge-guarded frontmatter
- status: promoted
- decision_reason: One-line logic fix — check phase_state before writing force-close trace. Regression from 2a72b794.
- next_action: B2_IBM → pr-create-guarded → pr-merge-guarded
- revisit_trigger: N/A
- acceptance_criteria:
  - wt-close --force skips frontmatter write when phase_state=absorbed
  - pr-merge-guarded frontmatter is never overwritten by wt-close
- promotion_gate: code change correct, gate passes
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260617T160003Z-A/issue.md
- milestone: M-20260617T160003Z-A
- session_refs: []
