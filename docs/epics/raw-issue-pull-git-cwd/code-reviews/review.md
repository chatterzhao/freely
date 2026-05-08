# Code Review: raw-issue-pull fix
- issue_id: I-20260508T133423Z-A
## Implementation Decision Note
- decision: Remove -C ROOT_DIR, add fix/feature guard
- why_this: -C ROOT_DIR always resolves to develop
- alternatives_considered: Keep -C but pass --worktree (rejected - fragile)
- boundary_non_goals: platform-adapter key standardization (#257)
- residual_risk: None
