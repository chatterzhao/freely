# Code Review: platform-adapter title key fix
- issue_id: I-20260508T121541Z-A
## Implementation Decision Note
- decision: Skip key standardization when title already has raw-{raw_key}
- why_this: Title is the canonical key source; created_at is imprecise
- alternatives_considered: Use created_at always (rejected — causes key mismatch)
- boundary_non_goals: wt-create pull flow, raw-issue-pull branch guard
- residual_risk: None
