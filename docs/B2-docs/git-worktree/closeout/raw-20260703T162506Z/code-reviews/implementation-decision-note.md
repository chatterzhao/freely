- issue_id: I-20260703T162506Z-A
## IDN
- decision: search _id = "agent_id" pattern
- why_this: matches actual toml format
- alternatives_considered: regex (overkill)
- boundary_non_goals: no other callers use this function
- residual_risk: if toml format changes, may need update
