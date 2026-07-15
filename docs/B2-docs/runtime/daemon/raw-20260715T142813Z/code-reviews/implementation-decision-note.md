- issue_id: I-20260715T142813Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/issues/I-20260715T142813Z-A.md

## Implementation Decision Note

- decision: Replace agent-id.env file reading with _resolve_current_agent_id function call in _init_agent_table_slot_pin

- why_this: _resolve_current_agent_id already properly reads agent_working SQLite table with agent-id.env fallback. Reusing it avoids duplicating the resolution logic.

- alternatives_considered: (a) Fix agent-id.env generation — rejected, table is the correct source. (b) Pass agent_id via env var — rejected, adds complexity.

- boundary_non_goals: Not changing _resolve_current_agent_id. Not changing agent_assign timing.

- residual_risk: Worker resolution depends on agent_assign being called before daemon start. This is a separate concern.
