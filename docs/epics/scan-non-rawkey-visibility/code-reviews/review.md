# Code Review
- issue_id: I-20260513T075847Z-A
## Implementation Decision Note
- decision: scan emits platform_only items for ALL open platform issues, not just those with raw-{key} pattern
- why_this: 33 open issues (50%) were silently invisible to scan because they lacked raw-YYYYMMDDTHHMMZ in title/body
- alternatives_considered: (1) Keep filtering by raw-key only — current broken behavior (2) Emit all with gh-{number} key — chosen
- boundary_non_goals: Not changing lifecycle chain trace (only platform_scan + classification), not changing completion detection
- residual_risk: Platform issues without raw-key have no lifecycle chain, so next_action is a manual hint instead of wt-create command
