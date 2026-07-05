---
issue_id: I-20260626T173930Z-A
issue_path: docs/issues/I-20260626T173930Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260626T173930Z-A
## Implementation Decision Note
- decision: 合并 _assemble_slot_test_command + _bridge_env_for_registered_tool 为 ai_cli_tool_with_auth_assemble(type, slot)。新增 _test_slot, _resolve_current_agent_id, _update_agent_table_slot。
- why_this: 消除分叉，slot recovery 基于实测而非盲选，agent-table 是唯一真相源。
- alternatives_considered: 保持两个函数（分叉），只改 recovery 不改 assembly（治标）
- boundary_non_goals: 不改 codex slot 路径（已有独立切换逻辑），不改 AI_FALLBACK_TOOLS
- residual_risk: _test_slot 每 30s 超时，多 slot 扫描可能较慢
