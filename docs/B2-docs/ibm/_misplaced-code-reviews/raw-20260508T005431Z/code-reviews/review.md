# Code Review: skill standardization
- issue_id: I-20260508T005431Z-A
## Implementation Decision Note
- decision: deploy skills to ~/.claude/skills/, use relative paths for cross-skill refs
- why_this: Skill tool only recognizes ~/.claude/skills/, project paths break after deploy
- alternatives_considered: symlinks (rejected: fragile), MCP server (rejected: overkill)
- boundary_non_goals: does not change skill content or add new skills
- residual_risk: none
