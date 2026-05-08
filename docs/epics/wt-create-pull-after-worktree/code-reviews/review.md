# Code Review: wt-create pull defer
- issue_id: I-20260508T124041Z-A
## Implementation Decision Note
- decision: Move pull from _require_issue_exists to after fix worktree creation, running from inside fix_target
- why_this: raw-issue-pull requires branch name containing raw-key, cannot run on develop
- alternatives_considered: Allow raw-issue-pull on develop with internal flag (rejected - weakens guard)
- boundary_non_goals: chat-inbox pull (already works), platform-adapter key standardization (#257)
- residual_risk: None
