# Tasks: adapter/ACP dispatch 注册表驱动化
- issue_id: I-20260624T090635Z-A

### T1: tool_supported_adapters() → registry adapters.supported
- 未注册默认 direct
- status: completed

### T2: tool_supported_launch_kinds_for_adapter() → registry adapters.launch_kinds
- status: completed

### T3: tool_run_acp_from_prompt_file() → 通用 ACP 路径
- claude/opencode 合并为通用路径，codex 保留独立
- status: completed

### T4: _resolve_tool_family() fallback → 扫描 registry aliases
- status: completed

### T5: tool_supports_add_dir_boundary() → registry
- status: completed

### T6: monitor-ai-acp.sh 移除 hardcoded permission fallback
- status: completed
