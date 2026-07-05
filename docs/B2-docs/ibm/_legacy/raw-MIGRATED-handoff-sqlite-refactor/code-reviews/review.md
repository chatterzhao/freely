# Code Review: handoff SQLite refactor
- issue_id: I-20260509T090210Z-A
## Implementation Decision Note
- decision: Replace file-based exit contracts with SQLite handoffs table. One table, role field distinguishes manager/worker. Absolute paths for worktree.
- why_this: Current awk regex markdown parsing is fragile. SQLite provides atomic writes, queryability, built-in validation.
- alternatives_considered: (1) JSON files — rejected, no queryability (2) Keep env files — rejected, already fragile (3) Two tables — rejected, role field simpler
- boundary_non_goals: Not changing continuity.md, not adding ACP session management
- residual_risk: Old env files remain as .bak; must be excluded from future scanning
