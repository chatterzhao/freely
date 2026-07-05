---
b1_id: B1-20260703T114618Z
phase_state: completed
source_raw: raw-20260703T114618Z18Z
produced_candidate: C-20260703T114618Z-A
---

# B1_IBM: 统一 agent_working 在 ACP session 创建时写入

## Problem

### 现状：agent_working 写入不一致

agent_working 表设计为 ACP session/new|fork 时写入（见 `agent_working.py:43`），
但实际写入点分散且不完整：

| ACP session 创建点 | 角色 | 写入 agent_working | 位置 |
|-------------------|------|:---:|------|
| `_handle_needs_manager` → `session/new` | manager | ✅ | `watchdog_sse.py:442` |
| `_handle_needs_worker` → `session/fork` | worker | ✅ (间接) | `watchdog_sse.py` |
| `_handle_needs_reviewer` → `session/fork` 或 `session/new` | reviewer | ✅ | `watchdog_sse.py:357-380` |
| **supervisor 循环 → `start-lead-agent.sh` → ACP `session/new` 或 `session/resume`** | **manager** | **❌ 不写** | `freely:20028` |

### 后果

1. **Manager 自己的 session 不注册**：daemon 启动后 supervisor 循环调用
   `start-lead-agent.sh` 启动 manager AI → ACP bridge 创建 session（new/resume）
   → session_id 只写入 `session-state.env` 和 `session-store`，不写入 `agent_working`

2. **`__manager__` 记录 lazy 创建**：只有 `_handle_needs_manager` 触发时才写——
   在此之前 fork 不可用（IDN residual_risk #1）

3. **重启恢复不统一**：worker/reviewer 的 session 可通过 `agent_working` 恢复，
   manager 的 session 只能通过 `session-store` + `session-state.env` 恢复

4. **会话注册表语义破碎**：`agent_working` 本应是"谁在用哪个 session"的通用注册表，
   但 manager session 不在其中

## 全量消费者分析

### 消费者 1：supervisor 循环 — manager AI 启动

```
freely: start_project_runtime()
  → 进入 supervisor while true 循环
  → build_prompt 系列函数
  → bash start-lead-agent.sh (line 20028)
    → 内部：启动 AI 工具 → AI 连接 ACP bridge → session/new 或 session/resume
  → start-lead-agent.sh 返回后 session_id 在 session-state.env 中
```

**当前**：session_id 写入 `session-state.env` + `session-store`，不写 `agent_working`
**应做**：在 `_persist_session_anchor_early()`（freely:3984）中同步写入 `agent_working.__manager__`

### 消费者 2：`_handle_needs_manager` — 其他 agent 需要 manager

```
watchdog_sse.py: _handle_needs_manager()
  → 读 agent_working.__manager__ → 有 session_id
  → session/resume + prompt（投递消息）
  → 无 session_id → session/new → agent_assign(__manager__)  ← 当前唯一写入点
```

**当前**：已正确写入（但 lazy）
**应做**：无需改——如果 consumer 1 已写入，这里读到的就是最新 session_id

### 消费者 3：`_handle_needs_worker` — manager 委派 worker

```
watchdog_sse.py: _handle_needs_worker()
  → session/fork from manager → agent_assign(raw_key, "worker")
```

**当前**：✅ 已正确实现，无需改

### 消费者 4：`_handle_needs_reviewer` — worker 需要审查

```
watchdog_sse.py: _handle_needs_reviewer()
  → 读 agent_working(raw_key, "reviewer") → session/resume
  → 无 → session/fork or session/new → agent_assign(raw_key, "reviewer")
```

**当前**：✅ 已正确实现，无需改

### 消费者 5：`_persist_session_anchor_early()` — ACP session ID 持久化

```
freely:3984: _persist_session_anchor_early()
  → 写 session-state.env (LAST_TOOL_SESSION_ID, CLAUDE_SESSION_ID_CURRENT)
  → 写 session-store (SQLite, via freely-db-cli)
```

**当前**：不写 `agent_working`
**应做**：这是 manager session 写入 agent_working 的最佳位置——
  每次 AI cycle 开始时调用，此时 session_id 已知

## Decision

**统一写入点：`_persist_session_anchor_early()`**

理由：
1. 这是每个 AI cycle 开始时的锚点——session_id 已知
2. 已经在此写入 `session-state.env` 和 `session-store`
3. 添加 `agent_working.__manager__` 写入只需一行 RPC 调用
4. 按角色区分：manager → `__manager__`，worker → issue raw_key

**不改 `_handle_needs_manager`**：它已经正确处理了"读 agent_working → session/resume + prompt"的流程

**不改 `watchdog_sse.py` 的 worker/reviewer 写入**：已正确

## Implementation

```bash
# 在 _persist_session_anchor_early() 中：
if [[ "$(effective_runtime_role_for_project "$project")" == "manager" ]]; then
  _raw_key="__manager__"
  _agent_id="manager_01"
else
  _raw_key="..."
  _agent_id="..."
fi
python3 -c "from agent_working import agent_assign; \
  agent_assign('$project', '$_raw_key', '$(FREELY_ROLE_HINT:-manager)', \
               '$_agent_id', session_id='${CLAUDE_SESSION_ID_CURRENT:-}')" 2>/dev/null || true
```

## Candidate
- candidate_id: C-20260703T114618Z-A
- status: promoted
- milestone: M-20260703T114618Z-A
