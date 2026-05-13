# Code Review
- issue_id: I-20260513T120734Z-A
## Implementation Decision Note
- decision: increase RESTART_STORM_COUNT from 4 to 10
- why_this: Normal daemon startup spawns 8+ infrastructure processes (supervisor, bridge, ACP server, claude, watchdog, dispatcher, monitor, run-acp-prompt). Storm threshold of 4 triggers false positives on every startup.
- alternatives_considered: (1) Exclude infrastructure processes from count — more invasive (2) Increase to 10 — minimal change
- boundary_non_goals: Not changing storm detection logic, window duration, or escalation behavior
- residual_risk: Actual restart storms with >10 rapid cycles in 30s window still trigger correctly
