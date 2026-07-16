- issue_id: I-20260716T020008Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260716T020008Z/issues/I-20260716T020008Z-A.md
## Implementation Decision Note
- decision: Extend capture_worker_session_id_and_store to call acp_session_register after session capture
- why_this: Function already captures session_id and validates UUID. Adding agent_working writeback at this point is natural. agent_assign writes basic entry before fork; this updates session_id after.
- alternatives_considered: Write from run-acp-prompt.py output directly — rejected, fragile string parsing
- boundary_non_goals: Not changing fork mechanism or worker launch path
- residual_risk: worker slot hardcoded to claude (same as manager bridge). Multi-tool worker needs separate bridge.
