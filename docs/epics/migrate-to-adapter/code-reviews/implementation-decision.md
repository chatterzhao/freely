---
issue_id: I-20260625T045412Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260625T045412Z-A
## Implementation Decision Note
- decision: cmd_feedback uses adapter create-issue; future commands follow
- why_this: single platform contact point; add platform = adapter only
- alternatives_considered: none
- boundary_non_goals: issue-sync migration deferred
- residual_risk: none
