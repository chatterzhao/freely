# Code Review: unified platform layer
- issue_id: `I-20260507T0700Z-A`
## Implementation Decision Note
- decision: Add Gitee title search + raw-issue-pull auto-sync + deprecate batch
- why_this: Ensures all configured platforms stay in sync
- alternatives_considered: Per-platform handling (rejected: too fragmented)
- boundary_non_goals: Full platform-adapter merge (separate refactor)
- residual_risk: Gitee search requires API availability
