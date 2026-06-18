# Implementation Decision
- issue_id: I-20260618T054147Z-A
- decision: Add git remote prune after remote branch deletion in wt-close Phase 4
- why_this: 67 stale tracking refs accumulated. git fetch doesn't prune by default.
- alternatives_considered: git config fetch.prune=true — rejected, affects all repos globally
- boundary_non_goals: Not pruning on every fetch, only on wt-close
- residual_risk: None
