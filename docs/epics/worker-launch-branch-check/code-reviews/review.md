# Code Review: worker launch branch check
- issue_id: I-20260509T022152Z-A
## Implementation Decision Note
- decision: Add branch prefix check in worker_prompt_launchable_for_manager_project
- why_this: Workers launched on develop/test-pre-merge can't commit, causing fast exit and restart storms
- alternatives_considered: (1) Auto-redirect to companion worktree — rejected, runtime shouldn't guess (2) Manager-side only — rejected, needs runtime enforcement as safety net
- boundary_non_goals: Not changing worker prompt generation, not changing exit contract format
- residual_risk: Manager may still delegate to wrong worktree, but runtime now rejects with clear error
