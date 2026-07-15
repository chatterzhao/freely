- issue_id: I-20260715T115327Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T115327Z/issues/I-20260715T115327Z-A.md
## Implementation Decision Note
- decision: Change line 22757 to use registry-resolved tool_adapter instead of unset AGENT_AI_TOOL_ADAPTER
- why_this: AGENT_AI_TOOL_ADAPTER never set (agent-table replaced config.toml AI_TOOL). tool_adapter resolved correctly via registry at line 22720.
- alternatives_considered: Set AGENT_AI_TOOL_ADAPTER in config — rejected, agent-table is the single source of truth
- boundary_non_goals: Not removing direct mode code (separate cleanup)
- residual_risk: None — tool_adapter always resolves to acp via registry
