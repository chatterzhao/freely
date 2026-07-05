---
issue_id: I-20260625T020000Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260625T020000Z-A
## Implementation Decision Note
- decision: pr-create-guarded IBM gate error block detects fix/feat, shows skill guidance
- why_this: users fix against error messages instead of reading skills
- alternatives_considered: modify governance-merge-gate output (too invasive, wrapper is better)
- boundary_non_goals: governance-merge-gate itself unchanged
- residual_risk: none
