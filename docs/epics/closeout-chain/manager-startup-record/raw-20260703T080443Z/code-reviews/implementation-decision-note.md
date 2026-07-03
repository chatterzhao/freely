- issue_id: I-20260703T080443Z-A

## Implementation Decision Note

- decision: daemon startup writes __manager__ UPSERT; inline _meta_env_value in start-lead-agent.sh
- why_this: manager is created at daemon startup, not lazily; subprocess needs its own function definitions
- alternatives_considered: source runtime functions → rejected (too many deps); lazily create → rejected (wrong semantics) → rejected (too many deps); lazily create → rejected (wrong semantics)
- boundary_non_goals: doesn't change session creation flow
- residual_risk: the updated_at timestamp is used for session tracking; concurrent restarts could race
