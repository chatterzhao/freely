# Code Review: wt-create --source parameter
- issue_id: `I-20260507T0730Z-A`
## Implementation Decision Note
- decision: Add --source required param with scan matching
- why_this: Forces AI to determine source, validates against scan
- alternatives_considered: Auto-detect (rejected: AI needs to explicitly understand source)
- boundary_non_goals: Multi-platform fill (#243)
- residual_risk: None
