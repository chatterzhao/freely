# Tasks: 多 ACP bridge 并行

- issue_id: I-20260704T080808Z-A

## Phase 1: socket/pid 命名 per-tool (8 处)

- [ ] freely `_acp_bridge_pid_file`: 签名改为 `(project, base_tool)`，命名含 `-{base_tool}`
- [ ] freely `_acp_bridge_socket`: 启用 base_tool（当前接受但忽略），返回 `-{base_tool}.sock`
- [ ] `acp-bridge.py` `_pid_file`: 加 `base_tool` 参数
- [ ] `acp-bridge.py` `_socket_path`: 加 `base_tool` 参数
- [ ] `monitor-ai-acp.sh` `_bridge_pid_file`: 加 `base_tool` 参数
- [ ] `monitor-ai-acp.sh` `_bridge_socket`: 加 `base_tool` 参数
- [ ] `watchdog_sse.py` `_acp_bridge_socket`: 加 `base_tool` 参数
- [ ] `agent_working.py` `_resolve_bridge_socket`: 启用 base_tool

## Phase 2: 硬编码 socket 替换 (4 处)

- [ ] freely line 13803: `bridge_socket="/tmp/freely-acp-{hash}.sock"` → `$(_acp_bridge_socket)`
- [ ] freely line 18872: reviewer session 硬编码 socket → `$(_acp_bridge_socket "$project" "$base_tool")`
- [ ] freely line 1807: cleanup rm socket 硬编码 → `$(_acp_bridge_socket)`
- [ ] freely line 1770: pid_file case 硬编码 → `$(_acp_bridge_pid_file)`

## Phase 3: daemon start 多 bridge 启动

- [ ] 扫描 agent-table.toml 所有 role slot → 提取 unique base_tools
- [ ] 对每个 base_tool 调用 `_ensure_acp_bridge_running "$project" "$bt"`
- [ ] `_tool_is_registered "$bt"` 检查 → 不可解析 → log_error + exit 1
- [ ] line 22152 daemon start: 单 bridge 调用 → 改为遍历所有 base_tool
- [ ] line 22241 cycle check: 同上，检测每个 bridge alive，重建 dead 的

## Phase 4: daemon stop + cleanup 多 bridge

- [ ] `_stop_acp_bridge` 参数化: `(project, base_tool)` — `""` = 全停
- [ ] line 5683 stop: 改为 `_stop_acp_bridge "$project" ""` (全停)
- [ ] line 5700 stop: 同上
- [ ] line 14085 tool change: `_stop_acp_bridge "$project" "$old_base_tool"` (只停旧的)
- [ ] line 14095 tool change: 同上
- [ ] line 21492 tool switch: 同上
- [ ] 切号后只停当前 tool bridge，不影响其他 agent
- [ ] `_cleanup_patterns` 更新：多 bridge 进程 + 多 pid/socket 文件清理
- [ ] line 14284, 21435-21443: pid/socket rm → per-tool 清理

## Phase 5: worker launch + reviewer session

- [ ] line 13179: `_manager_bridge_socket` → 传入 worker_base_tool
- [ ] line 18872: reviewer session 硬编码 → 传入 reviewer_base_tool
- [ ] line 13192: `--bridge-socket` 参数 → worker 的 base_tool 对应 socket

## Phase 6: 测试验证

- [ ] AT-001: socket/pid 命名含 base_tool
- [ ] AT-002: N 个 base_tool → N 个 bridge
- [ ] AT-003: 不可解析 base_tool → hard error
- [ ] AT-004: _stop_acp_bridge 参数化
- [ ] AT-005: _resolve_bridge_socket 启用
- [ ] 单 bridge 向后兼容 (agent-table 只有一个 base_tool)
- [ ] 多 bridge 正常启停
- [ ] 切号不影响其他 agent bridge
