# Tasks: 多 ACP bridge 并行

- issue_id: I-20260704T080808Z-A

## Phase 1: socket/pid per-tool
- [ ] _acp_bridge_pid_file: 命名含 base_tool
- [ ] _acp_bridge_socket: 命名含 base_tool
- [ ] agent_working.py _resolve_bridge_socket: 启用 base_tool

## Phase 2: daemon start 多 bridge
- [ ] 扫描 agent-table 所有 slot → 提取唯一 base_tool
- [ ] 对每个 base_tool 调用 _ensure_acp_bridge_running
- [ ] _tool_is_registered 检查 → 不可解析 → hard error exit 1
- [ ] config.toml FREELY_ACP_{TOOL}_BIN 检查

## Phase 3: daemon stop 多 bridge
- [ ] _stop_acp_bridge 参数化 (base_tool)
- [ ] daemon stop 遍历所有 base_tool 调用 _stop_acp_bridge
- [ ] cleanup 模式更新 (多 pid/socket 文件)

## Phase 4: 切号兼容
- [ ] 切号后的 _stop_acp_bridge 改为只停当前 tool
- [ ] 切号不影响其他 agent 的 bridge

## Phase 5: 测试验证
- [ ] AT-001~AT-005 全部 GREEN
- [ ] 单 bridge 行为向后兼容 (agent-table 只有一个 base_tool)
- [ ] 多 bridge 正常启停
