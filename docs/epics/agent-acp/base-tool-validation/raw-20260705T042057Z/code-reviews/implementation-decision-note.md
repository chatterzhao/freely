---
issue_id: I-20260705T042057Z-A
issue_path: docs/epics/agent-acp/base-tool-validation/raw-20260705T042057Z/issues/I-20260705T042057Z-A.md
phase_state: in_dev
---
- issue_id: I-20260705T042057Z-A
## Implementation Decision Note
- decision: Add _validate_base_tool_from_slot to validate slot naming convention and tool-registry at all entry points
- why_this: base_tool extracted from slot was not validated, unsupported tools would silently fail
- alternatives_considered: Validate only at daemon start → misses worker launch and cycle check
- boundary_non_goals: Does not change session routing or fork logic
- residual_risk: None
