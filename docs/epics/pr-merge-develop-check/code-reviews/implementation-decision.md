# Implementation Decision
- issue_id: I-20260618T044047Z-A
- decision: Add cd to PROJECT_ROOT via git worktree list + develop cleanliness check
- why_this: pr-merge uses $PWD without explicit cd. If run from worktree, would check wrong dir
- alternatives_considered: Use config.toml — rejected, slower startup
- boundary_non_goals: Not changing other $PWD usages
- residual_risk: None
