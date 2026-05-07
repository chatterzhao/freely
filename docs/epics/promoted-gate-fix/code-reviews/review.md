# Code Review: promoted gate fix
- issue_id: `I-20260507T0200Z-A`
## Implementation Decision Note
- decision: Add candidate_issues check for promoted candidates
- why_this: Fixes bypass where promoted candidate skips C→M queue
- alternatives_considered: None
- boundary_non_goals: Other gate checks unchanged
- residual_risk: None
