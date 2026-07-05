---
issue_id: I-20260625T031400Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260625T031400Z-A
## Implementation Decision Note
- decision: use gh and gitee-issue.py directly, not adapter create-issue (doesn't exist)
- why_this: platform-adapter has no create-issue CLI subcommand
- alternatives_considered: add create-issue to adapter (bigger change)
- boundary_non_goals: platform-adapter unchanged
- residual_risk: none
