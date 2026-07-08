# Implementation Decision Note
- issue_id: I-20260708T174039Z-A
- decision: 在 tool_run_acp_from_prompt_file() 中将 _bridge_socket "$project" 改为 _bridge_socket "$project" "$tool"，其中 $tool 已通过 _resolve_tool_family 解析为 base family name。
- why_this: 这是最小修改（一行），且与其他所有 call site（acp-bridge.py、freely、monitor-ai-acp.sh、watchdog_sse.py、agent_working.py）保持一致——它们都传 base_tool。commit 191afb82c 更新了 5 个文件但遗漏了 tool-launchers.sh。
- alternatives_considered: (1) 改 _bridge_socket 函数默认值让它在不传 base_tool 时自动检测 → 引入隐式依赖，不推荐；(2) 像 codex 分支那样硬编码 socket 路径 → 重复代码。上述都不如直接传入 $tool 简洁。
- boundary_non_goals: 不修改 _bridge_socket 函数签名；不修改其他 5 个已有的正确 call site；不修改 codex 的特殊 socket 路径。
- residual_risk: 无。修复后所有 ACP tool (claude, opencode, codex) 的 socket 路径与 bridge 监听路径完全一致。codex 分支已有自己的 socket 路径逻辑，不受影响。
