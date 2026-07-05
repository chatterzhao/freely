---
name: Pre-merge Gate Check Implementation Decision Note
owner_issue: I-20260616T033325Z-A
owner_issue_path: docs/issues/I-20260616T033325Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: premerge-gate-check-review
---

# Implementation Decision Note: Pre-merge Governance Gate

- issue_id: I-20260616T033325Z-A
- issue_path: docs/issues/I-20260616T033325Z-A/issue.md
- source_candidate: docs/pre-brainstorms/20260616T033325Z--premerge-gate-check/candidates.md

## Implementation Decision Note

- decision: Add governance-merge-gate check in pr-create-guarded Step 2b and FREELY_SKIP_IBM_GATE path in pre-commit hook
- why_this: Governance gaps discovered at push time cause repetitive fix cycles. Early detection with clear skill references prevents this.
- alternatives_considered: Run gate only at push time (rejected: too late); Gate check in pr-merge-guarded only (rejected: PR already created)
- boundary_non_goals: Does not change gate logic itself; Does not affect direct develop workflow for wt-close automated commits
- residual_risk: If governance-merge-gate itself is broken, pre-commit could block legitimate governance commits
