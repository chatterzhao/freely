- issue_id: I-20260716T005354Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260716T005354Z/issues/I-20260716T005354Z-A.md
## Implementation Decision Note
- decision: Remove return 0 from acp_session_register else branch so worker/reviewer session_ids are written to agent_working
- why_this: agent_assign in worker launch writes basic entry; acp_session_register should update with session_id after session creation
- alternatives_considered: Rewrite entire worker launch to use acp_session_connect — deferred to separate PR
- boundary_non_goals: Not changing worker launch path. Not implementing acp_session_connect integration.
- residual_risk: worker session_id written without cross-tool detection (always fork from Claude)
