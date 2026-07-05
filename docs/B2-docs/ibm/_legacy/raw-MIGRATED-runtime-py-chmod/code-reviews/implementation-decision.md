---
issue_id: I-20260624T154500Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260624T154500Z-A
## Implementation Decision Note
- decision: commit 100644→100755 mode change
- why_this: git tracks execute bit; without commit, every checkout reverts
- alternatives_considered: none (only correct fix)
- boundary_non_goals: no code changes
- residual_risk: none
