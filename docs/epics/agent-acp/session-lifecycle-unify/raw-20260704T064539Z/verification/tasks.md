# Tasks: 统一 ACP session 管理

- issue_id: I-20260704T064539Z-A

## Phase 1: agent_working.py 新增方法

### Task 1.1: acp_session_register() 统一写入入口
- [x] 新增 `acp_session_register(project, raw_key, role, agent_id, session_id, slot, worktree, branch)` 
- [x] 内部调用 `agent_assign`，传入完整参数（含 slot）
- [x] 参数默认值: worktree="", branch="", 保持向后兼容

### Task 1.2: acp_session_connect() 决策树
- [x] 新增 `acp_session_connect(project, raw_key, role, agent_id, slot, message, force_new, parent_role)`
- [x] 实现 force_new → session/new
- [x] 实现 alive session → prompt (有 message) / return (无 message)
- [x] 实现 dead session → resume → ok 或 fallback new + log
- [x] 实现 no session + same base_tool → fork(Mgr) → ok 或 fallback new + log
- [x] 实现 no session + cross base_tool → new + log
- [x] `_resolve_bridge_socket(project, base_tool)` — 本期返回唯一 socket

## Phase 2: DB schema

### Task 2.1: agent_working 表加 slot 列
- [x] `ALTER TABLE agent_working ADD COLUMN slot TEXT DEFAULT ''`
- [x] `h_aw_upsert` INSERT 写入 slot
- [x] `h_aw_upsert` UPDATE 写入 slot + 同步更新 worktree/branch

### Task 2.2: DB migration 兼容性
- [x] 已有行 slot 为空不报错（DEFAULT ''）
- [x] log_info 记录首次 migration

## Phase 3: watchdog_sse.py 重构

### Task 3.1: 删除 6 个旧函数
- [x] 删除 `_acp_session_new()` (~12 lines)
- [x] 删除 `_acp_session_fork()` (~30 lines)
- [x] 删除 `_acp_session_resume()` (~15 lines)
- [x] 删除 `_acp_session_prompt()` (~10 lines)
- [x] 删除 `_should_use_fork()` (~25 lines)
- [x] 删除 `_create_reviewer_session()` (~50 lines)

### Task 3.2: 重构 3 个 handler
- [x] `_handle_needs_reviewer`: 改为调用 `acp_session_connect`
- [x] `_handle_needs_worker`: 改为调用 `acp_session_connect`
- [x] `_handle_needs_manager`: 改为调用 `acp_session_connect`
- [x] 保留 agent_next_free 分配逻辑（在 acp_session_connect 之外）
- [x] 保留 task message 构建逻辑

## Phase 4: freely shell bridge 解耦

### Task 4.1: _ensure_acp_bridge_running 参数化
- [x] 签名改为 `_ensure_acp_bridge_running(project, base_tool)`
- [x] 内部 `local base_tool="${2:-claude}"` 替代 `AGENT_AI_TOOL`
- [x] daemon start 调用: `_ensure_acp_bridge_running "$project" "${AGENT_AI_TOOL%%-*}"`
- [x] cycle check 调用: 同上

### Task 4.2: _acp_bridge_socket 预留参数
- [x] 签名改为 `_acp_bridge_socket(project, base_tool)`
- [x] 本期 base_tool 参数被忽略，返回相同 socket
- [x] 所有调用方传入 base_tool（预留，行为不变）

### Task 4.3: _persist_session_anchor_early 重构
- [x] Manager 写入改为调用 `acp_session_register`（含 slot=AGENT_AI_TOOL）
- [x] Worker/Reviewer 写入移除（由 watchdog 的 acp_session_connect 处理）

### Task 4.4: worker launch + reviewer session 重构
- [x] worker launch: 通过 `_acp_bridge_socket(project, worker_base_tool)` 获取 socket
- [x] reviewer: 同样改为 `_acp_bridge_socket(project, reviewer_base_tool)`

## Phase 5: 命名替换

### Task 5.1: CLAUDE_SESSION_ID_CURRENT → TOOL_SESSION_ID_CURRENT
- [x] `freely`: 全部引用替换
- [x] `session-cache.sh`: 全部引用替换
- [x] `monitor-ai-cli.sh`: 全部引用替换
- [x] 验证: `grep -rn "CLAUDE_SESSION_ID_CURRENT" docs/system/workspace/scripts/ | wc -l` = 0

## Phase 6: 清理验证

### Task 6.1: 删除无用引用
- [x] 确认无残留的旧 session 函数引用
- [x] 确认 agent-id.env 不再需要（agent_working 是唯一真源）

### Task 6.2: 日志一致性
- [x] 所有 fallback 路径有日志
- [x] Manager restart 有 resume/session 选择日志
- [x] slot 变化有日志
