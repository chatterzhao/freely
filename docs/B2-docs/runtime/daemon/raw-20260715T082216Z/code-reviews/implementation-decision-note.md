- issue_id: I-20260715T082216Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/issues/I-20260715T082216Z-A.md

## Implementation Decision Note

- decision: Add _load_slot_env_vars to tool-launchers.sh, use in _bridge_ensure_running

- why_this: monitor-ai-acp.sh sources tool-launchers.sh (not freely script), so ai_cli_tool_with_auth_assemble unavailable. New function reads same registry fields without duplicating logic.

- alternatives_considered: (a) Call freely script from monitor-ai-acp.sh — rejected, creates circular dependency. (b) Only fix _apply_tool_alias_settings — rejected, still depends on aliases. (c) Move ai_cli_tool_with_auth_assemble to tool-launchers.sh — rejected, too invasive.

- boundary_non_goals: NOT removing _apply_tool_alias_settings (keep as optional alias path). NOT changing _ensure_acp_bridge_running.

- residual_risk: _load_slot_env_vars duplicates the JSON-reading logic from ai_cli_tool_with_auth_assemble. Future registry schema changes need to update both.
