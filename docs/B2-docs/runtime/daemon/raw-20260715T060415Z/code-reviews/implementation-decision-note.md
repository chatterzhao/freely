- issue_id: I-20260715T060415Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T060415Z/issues/I-20260715T060415Z-A.md
## Implementation Decision Note
- decision: Align 3 field names between scan script output and injection code
- why_this: scan script uses total/by_station/station; injection code read total_incomplete/by_stage/stage
- alternatives_considered: Change scan script instead — rejected (more invasive)
- boundary_non_goals: Not changing scan script schema
- residual_risk: Backward compat ensures old scan data still readable
