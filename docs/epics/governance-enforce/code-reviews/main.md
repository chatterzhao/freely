---
name: Governance Enforcement Implementation Decision Note
owner_issue: I-20260616T083810Z-A
owner_issue_path: docs/issues/I-20260616T083810Z-A/issue.md
implementation_decision_note: true
phase_state: completed
review_id: governance-enforce-review
---

# Implementation Decision Note: Governance Enforcement

- issue_id: I-20260616T083810Z-A
- issue_path: docs/issues/I-20260616T083810Z-A/issue.md
- source_candidate: docs/pre-brainstorms/20260616T083810Z--governance-enforce/candidates.md

## Implementation Decision Note

- decision: Clarify fix-execution timing + add IBM skill guidance to gate error messages
- why_this: SKIP_IBM_GATE abused because constraints unclear; error messages silent; fix-execution "later" misread as optional
- alternatives_considered: Remove SKIP_IBM_GATE entirely (rejected: needed for governance-automated commits); Only update docs (rejected: error messages also needed)
- boundary_non_goals: Does not change gate logic; Does not change governance-only path classification
- residual_risk: Skill guidance is advisory — enforcement depends on developer following instructions
