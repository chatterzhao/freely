- issue_id: I-20260716T000513Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/issues/I-20260716T000513Z-A.md
## Implementation Decision Note
- decision: Add agent_assign call in launch_worker_from_manager_prompt_if_needed before fork session launch
- why_this: agent_assign was only called in sync_project_tooling_from_source which is not triggered during worker delegation. Placing it in the worker launch path ensures agent_working is written before the worker process starts.
- alternatives_considered: (a) Fix sync_project_tooling call chain — rejected, too many dependencies. (b) agent_assign in _handle_needs_worker SSE path — rejected, that path uses separate daemon which doesn't always start.
- boundary_non_goals: Not changing worker tool selection (still uses Claude via fork). Not changing verification contract logic.
- residual_risk: Worker always gets Claude slot. Multi-tool worker support needs separate daemon per tool.
