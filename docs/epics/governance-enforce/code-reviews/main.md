---
name: Governance Enforcement Implementation Decision Note
owner_issue: I-20260616T083810Z-A
implementation_decision_note: true
phase_state: completed
review_id: governance-enforce-review
---

- issue_id: I-20260616T083810Z-A
- issue_path: docs/issues/I-20260616T083810Z-A/issue.md
- source_candidate: docs/pre-brainstorms/20260616T083810Z--governance-enforce/candidates.md

## Implementation Decision Note

- decision: Clarify fix-execution timing + add IBM skill guidance to gate error messages + rename docs/cleanup/format to document|cleanup|format
- why_this: SKIP_IBM_GATE was abused because constraints were unclear and error messages didn't tell developers what to do
- alternatives_considered: Remove SKIP_IBM_GATE entirely (rejected: legitimate for governance-automated commits); Only update docs (rejected: error messages also needed)
- boundary_non_goals: Does not change gate logic itself; Does not change what paths are governance-only
- residual_risk: Skill guidance in error messages is advisory only — enforcement still depends on developer following instructions
