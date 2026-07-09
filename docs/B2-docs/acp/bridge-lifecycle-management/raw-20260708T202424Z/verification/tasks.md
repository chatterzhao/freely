# Tasks: Agent Lifecycle (Lazy-Start + Idle-Sleep + Auto-Wake)
- issue_id: I-20260708T202424Z-A

## Task Breakdown

### 1. acp-bridge.py: Idle Monitor Thread
- [x] 在 `AcpBridge` 类中新增 `_idle_monitor_loop()` 方法
- [x] 在 `start_server()` 中启动 `_idle_thread`
- [x] 日志格式：`"idle {N}s (limit={ACP_IDLE_TIMEOUT}s) — no task for base_tool={base_tool}, shutting down, restart on next task"`
- [x] 设置 `self._idle_timeout_detected = True` + `self.running = False`
- [x] 新增 `ACP_IDLE_SHUTDOWN_GRACE = 30` 常量

### 2. freely: Daemon Startup Lazy-Start
- [x] daemon startup section (line 22281-22291)：识别 manager_01 的 base_tool
- [x] 只对 manager 的 base_tool 调用 `_ensure_acp_bridge_running`
- [x] 其他 base_tool 打印 `log_info "deferring bridge start (lazy-start)"`
- [x] cycle check (line 22388-22408) 保持不变

### 3. freely: _sync_project_tooling Auto-Wake
- [x] 替换 `grep agent-id.env` 轮询为 `agent_working.agent_next_free()` 调用
- [x] 解析 worker slot → base_tool
- [x] 调用 `_ensure_acp_bridge_running` 检查/启动 bridge
- [x] Bridge 启动失败 → `log_warn` + `return 1`
- [x] 保留 agent-id.env + agent_working dual-write

### 4. monitor-ai-acp.sh: Idle-Shutdown Detection
- [x] `_detect_acp_failure` 新增 idle-shutdown 模式匹配
- [x] 匹配 `"shutting down, restart on next task"` → 打印 info → 不设置 failure marker
- [x] 不影响其他错误检测逻辑

### 5. Verification
- [x] RED 阶段：全部 6 个 acceptance items 确认 RED（AT-005 除外，它是退化验证）
- [x] dev 实现
- [x] GREEN 阶段：全部 6 个 acceptance items PASS
- [x] pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
