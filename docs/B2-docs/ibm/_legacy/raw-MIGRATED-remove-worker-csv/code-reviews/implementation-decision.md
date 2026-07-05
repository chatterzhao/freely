# Implementation Decision: Remove worker_prompts_csv leftovers
- issue_id: I-20260617T121221Z-A
- decision: Remove all worker_prompts_csv from A2A layer (a2a_server, a2a_types, a2a_task, db_manager, docs)
- why_this: Field unused since #2914, 7 leftover locations
- alternatives_considered: Keep as dead code — rejected: confusion risk
- boundary_non_goals: DB column stays (backward compat), DB stops writing
- residual_risk: None — field already unused by runtime
