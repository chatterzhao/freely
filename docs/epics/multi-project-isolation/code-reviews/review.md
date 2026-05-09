# Code Review: multi-project isolation architecture
- issue_id: I-20260509T024559Z-A
## Implementation Decision Note
- decision: Define three-layer isolation model (git repo + raw-key + ACP session cwd) for multi-project concurrent development. No new mechanisms needed.
- why_this: Current daemon binds to single test worktree. Multi-project, multi-issue requires project-root-based daemon with raw-key worktree lookup.
- alternatives_considered: (1) One daemon per project — rejected, resource waste (2) Worktree registry in DB — already have handoffs table (#267)
- boundary_non_goals: Not implementing the full daemon refactor in this issue — architecture design only
- residual_risk: Implementation scope is large; phased rollout needed
