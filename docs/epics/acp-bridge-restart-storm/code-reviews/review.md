# Code Review
- issue_id: I-20260508T225041Z-A
## Implementation Decision Note
- decision: Worker prompt for test-pre-merge auto-includes companion writable worktree path
- why_this: AI gets WORKER_PROMPTS_NOT_LAUNCHABLE but doesn't know where the writable worktree is
- alternatives_considered: (1) Runtime auto-redirect — more invasive, requires session restart (2) Manager-side lookup — chosen, minimal change to prompt generation
- boundary_non_goals: Not changing worker launch flow, not modifying storm thresholds, not handling cache hit issue (#263)
- residual_risk: If companion worktree was deleted, prompt will lack the path — handled by `if [[ -n "$companion_wt" ]]` guard
