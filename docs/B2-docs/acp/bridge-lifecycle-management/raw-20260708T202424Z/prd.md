---
issue_id: I-20260708T202424Z-A
phase_state: done_b2_ibm
source_candidate: docs/B1-docs/raw-20260708T202424Z/candidates.md#C-20260708T202424Z-A
created_at: 2026-07-08
---

# PRD: Agent Lifecycle (Lazy-Start + Idle-Sleep + Auto-Wake)

- issue_id: I-20260708T202424Z-A

## Goal

让 ACP bridge 实现按需启动、空闲优雅退出、按需自动唤醒，配合 agent_working 表实现 agent pool 利用。

## 实现方案

### 改动 1: acp-bridge.py — Idle Monitor

在 `AcpBridge.start_server()` 中启动 daemon thread `_idle_monitor_loop()`：
- 每 30s 检查 `last_activity_ts`
- 空闲 > `ACP_IDLE_TIMEOUT + 30s` → `log("idle ... — shutting down, restart on next task")` → `self.running = False`

`stop_server()` 已有完整清理逻辑：`_kill_descendants` → `os.unlink(socket)` → `os.unlink(pid_file)`。

### 改动 2: freely daemon startup — Lazy-Start

位置：`freely` daemon 启动 section (line 22281-22291)。

当前逻辑：遍历 `_unique_tools`，每个都 `_ensure_acp_bridge_running`。
新逻辑：只对 manager_01 的 base_tool 执行 `_ensure_acp_bridge_running`；其他 tool 打 log 表示 defer。

Cycle check (line 22388-22408) 保持不变：只维护已启动的 bridge，不主动启动 lazy bridge。

### 改动 3: freely:_sync_project_tooling — Auto-Wake

位置：`freely` agent assignment section (line 6005-6032)。

当前逻辑：`grep agent-id.env` 选第一个不在文件中的 worker。
新逻辑：
1. `agent_working.agent_next_free()` 获取空闲 worker
2. 解析 worker slot → base_tool
3. `_ensure_acp_bridge_running` 检查/启动 bridge
4. Bridge 就绪后 dual-write agent-id.env + agent_working

### 改动 4: monitor-ai-acp.sh — Idle-Shutdown Detection

位置：`_detect_acp_failure` 函数。

新增：在检测 fatal errors 之前，先检查 `"shutting down, restart on next task"` 日志。匹配 → 打印 info 日志 → 不设置任何 failure marker → 不影响 cycle 流程。

## Dev-Loop Handoff

实现顺序：1 → 2 → 3 → 4（无强依赖，可任意顺序）
测试工位：`test-pre-merge-20260708T202424Z-agent-lifecycle`
测试策略：先用 `freely daemon start --task-mode wait` 验证 lazy-start；再模拟委派验证 auto-wake。
