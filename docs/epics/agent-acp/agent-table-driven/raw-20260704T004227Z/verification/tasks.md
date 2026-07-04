# Tasks: ACP Bridge 启动链路修复

- issue_id: I-20260704T004227Z-A

## Phase 1: monitor-ai-acp.sh `_bridge_ensure_running` 对齐

### Task 1.1: tool name 对比改为 base_tool
- [x] 修改 `_bridge_ensure_running` line 70-72: 从 `$last_tool` 和 `$tool` 各提取 `%%-*` 后再比较
- [x] 确保 tool 变化检测仍工作: base_tool 不同时仍触发重启

### Task 1.2: 增加 ACP binary 三层解析
- [x] 从 `$tool` 提取 `base_tool = "${tool%%-*}"`
- [x] registry 查询: `_tool_registry_get "$base_tool" "acp.binary"`
- [x] config.toml 查询: `awk` 读取 `FREELY_ACP_{TOOL}_BIN`
- [x] fallback: `command -v` 或默认 `claude-agent-acp`
- [x] 解析 acp.args (对 opencode 取 `"acp"`)
- [x] 传入 `--acp-bin "$acp_bin"` + `--acp-args "${acp_args[*]}"`

### Task 1.3: 写 .bin 文件
- [x] bridge 启动成功后写 `$acp_bin` 到 `$acp_bin_file`
- [x] 更新架构注释 (line 8: "→ claude-agent-acp" 改为 "→ tool-registry driven ACP binary")

## Phase 2: 环境变量清理

### Task 2.1: freely `_ensure_acp_bridge_running` 环境清理
- [x] 在 bridge env 组装后 (line ~14154), 启动前 (line ~14175), 插入 unset 循环
- [x] 清理变量列表: ANTHROPIC_* (7个), CLAUDE_CODE_* (6个), AI_AGENT
- [x] 保留 CLAUDE_CODE_PERMISSION_MODE
- [x] 加 log_info 记录清理的变量数

### Task 2.2: monitor-ai-acp.sh `_bridge_ensure_running` 环境清理
- [x] 同样 unset 逻辑，在 bridge 启动前 (line ~88)

## Phase 3: agent-id grep 精确匹配

### Task 3.1: load_config grep 修复
- [x] `grep -F "$(pwd)"` → `grep -F "$(pwd)="` (line 4278)

### Task 3.2: _init_agent_table_slot_pin grep 修复
- [x] 同样改为 `grep -F "$(pwd)="` (line 4779)

## Phase 4: 诊断日志

### Task 4.1: monitor-ai-acp.sh 日志
- [x] bridge 启动前: `[bridge] starting: base_tool=$base_tool acp_bin=$acp_bin acp_args=${acp_args[*]} slot=$tool config=$config_path`
- [x] bridge 切换时: `[bridge] tool changed ($last_base → $cur_base), restarting bridge`

### Task 4.2: freely 日志
- [x] `_ensure_acp_bridge_running`: 增加 sanitized_vars_count, kept_vars, config_path, model
- [x] `append_runtime_event acp_bridge_started`: 增加 binary_path, base_tool, slot
