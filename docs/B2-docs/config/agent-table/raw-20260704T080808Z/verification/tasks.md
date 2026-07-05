# Tasks: 多 ACP bridge 并行

- issue_id: I-20260704T080808Z-A

## Phase 1: socket/pid 命名 per-tool (8 处)

- [x] freely `_acp_bridge_pid_file`: 签名改为 `(project, base_tool)`，命名含 `-{base_tool}`
- [x] freely `_acp_bridge_socket`: 启用 base_tool（当前接受但忽略），返回 `-{base_tool}.sock`
- [x] `acp-bridge.py` `_pid_file`: 加 `base_tool` 参数
- [x] `acp-bridge.py` `_socket_path`: 加 `base_tool` 参数
- [x] `monitor-ai-acp.sh` `_bridge_pid_file`: 加 `base_tool` 参数
- [x] `monitor-ai-acp.sh` `_bridge_socket`: 加 `base_tool` 参数
- [x] `watchdog_sse.py` `_acp_bridge_socket`: 加 `base_tool` 参数
- [x] `agent_working.py` `_resolve_bridge_socket`: 启用 base_tool

## Phase 2: 硬编码 socket 替换 (4 处)

- [x] freely line 13803: `bridge_socket="/tmp/freely-acp-{hash}.sock"` → `$(_acp_bridge_socket)`
- [x] freely line 18872: reviewer session 硬编码 socket → `$(_acp_bridge_socket "$project" "$base_tool")`
- [x] freely line 1807: cleanup rm socket 硬编码 → `$(_acp_bridge_socket)`
- [x] freely line 1770: pid_file case 硬编码 → `$(_acp_bridge_pid_file)`

## Phase 3: daemon start 多 bridge 启动

- [x] 扫描 agent-table.toml 所有 role slot → 提取 unique base_tools
- [x] 对每个 base_tool 调用 `_ensure_acp_bridge_running "$project" "$bt"`
- [x] `_tool_is_registered "$bt"` 检查 → 不可解析 → log_error + exit 1
- [x] line 22152 daemon start: 单 bridge 调用 → 改为遍历所有 base_tool
- [x] line 22241 cycle check: 同上，检测每个 bridge alive，重建 dead 的

## Phase 4: daemon stop + cleanup 多 bridge

- [x] `_stop_acp_bridge` 参数化: `(project, base_tool)` — `""` = 全停
- [x] line 5683 stop: 改为 `_stop_acp_bridge "$project" ""` (全停)
- [x] line 5700 stop: 同上
- [x] line 14085 tool change: `_stop_acp_bridge "$project" "$old_base_tool"` (只停旧的)
- [x] line 14095 tool change: 同上
- [x] line 21492 tool switch: 同上
- [x] 切号后只停当前 tool bridge，不影响其他 agent
- [x] `_cleanup_patterns` 更新：多 bridge 进程 + 多 pid/socket 文件清理
- [x] line 14284, 21435-21443: pid/socket rm → per-tool 清理

## Phase 5: worker launch + reviewer session

- [x] line 13179: `_manager_bridge_socket` → 传入 worker_base_tool
- [x] line 18872: reviewer session 硬编码 → 传入 reviewer_base_tool
- [x] line 13192: `--bridge-socket` 参数 → worker 的 base_tool 对应 socket

## Phase 6: 测试验证

- [x] AT-001: socket/pid 命名含 base_tool
- [x] AT-002: N 个 base_tool → N 个 bridge
- [x] AT-003: 不可解析 base_tool → hard error
- [x] AT-004: _stop_acp_bridge 参数化
- [x] AT-005: _resolve_bridge_socket 启用
- [x] 单 bridge 向后兼容 (agent-table 只有一个 base_tool)
- [x] 多 bridge 正常启停
- [x] 切号不影响其他 agent bridge
