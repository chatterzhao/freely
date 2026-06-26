---
issue_id: I-20260625T211802Z-A
issue_path: docs/issues/I-20260625T211802Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260625T211802Z-A
- issue_path: docs/issues/I-20260625T211802Z-A/issue.md
## Implementation Decision Note
- decision: agent-table-query --next-free scans worktrees for worker-id.env; sync_tooling writes it; pr-review-guarded reads reviewer_slot
- why_this: makes agent-table operational for slot assignment
- alternatives_considered: centralized lock manager → over-engineered for v1
- boundary_non_goals: not implementing full Manager slot switching
- residual_risk: works with 1 pool; multi-pool support future enhancement
