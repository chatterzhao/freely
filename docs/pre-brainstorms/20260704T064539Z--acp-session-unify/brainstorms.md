---
b1_id: B1-20260704T064539Z
phase_state: completed
source_raw: raw-20260704T064539Z
source_url: https://github.com/chatterzhao/freely/issues/3726
produced_candidate: C-20260704T064539Z-A
created_at: 2026-07-04
---

# B1_IBM: 统一 ACP session 管理方法

## Input
- raw-20260704T064539Z (GitHub #3726)

## Problem

### 全局理解：Freely agent 通信模型

```
agent-table.toml 配置 manager/worker/reviewer 的 slot
       ↓
  freely daemon 启动 → 创建 ACP bridge
       ↓
  Manager 创建 session (new/resume)
       ↓
  A2A SSE 事件流 → watchdog_sse.py 监听
       ↓
  需要 Worker? → 选 session 操作 (fork/new/prompt)
       ↓
  Worker 完成 → 需要 Reviewer?
       ↓
  通过 session/prompt 把 verdict 发给 Reviewer session
```

### 四种 ACP session 操作

| 操作 | 何时用 | 缓存命中 | 约束 |
|------|--------|:---:|------|
| `session/new` | 首次、slot 变了、跨 tool 无法 fork | ❌ 冷启动 | 任何情况 |
| `session/fork` | Worker/Reviewer 从 Manager fork | ✅ 继承 context | **只能同 tool fork**，跨 tool 报错 |
| `session/resume` | 重启后恢复、session 死了唤醒 | ✅ 恢复历史 | **必须 slot 没变**，变了会报错 |
| `session/prompt` | 向 alive session 发消息 | N/A | session 必须 alive |

### 当前问题

**1. 没有统一的 session 操作选择逻辑。** 每个调用点自己判断，逻辑重复、不完整。

**2. agent_working 表没有 slot 列。** 无法判断 session 创建时用的 slot 是否与当前 agent-table 配置一致。重启时不知道能不能安全 resume。

**3. 没有跨 slot 检测。** 同 tool 不同 slot（如 opencode-apikey-ds-flash vs opencode-apikey-openai-gpt）fork 可能可以，但 resume 不行（因为 settings 变了）。跨 tool（opencode → claude）fork 和 resume 都不行。

**4. 会话恢复效率低。** Manager 每次启动都 session/new，不检查 agent_working 里有没有可以 resume 的 session。浪费上下文和缓存。

## Brainstorm

### 统一方法抽象

核心思想：一个方法，传入当前上下文，内部决策用哪种操作。

```python
def acp_session_connect(project, raw_key, role, agent_id, 
                        current_slot, message=None):
    """
    统一的 ACP session 生命周期管理。

    决策树:
    1. 查 agent_working: 有没有 {role}_id 记录？有没有 session_id？
       → 有 session_id:
         a. agent_working.slot == current_slot（slot 没变）?
            → session alive? → session/prompt(message) 或直接返回
            → session dead?  → session/resume → 更新 session_id
         b. agent_working.slot != current_slot（slot 变了）?
            → session/new（不能 resume/fork，配置已变）
       → 无 session_id:
    2. 能 fork 吗？
       a. 同 tool (base_tool 相同)?
          → session/fork from Manager（缓存命中）
       b. 跨 tool?
          → session/new（fork 不支持跨 tool）
    3. 成功 → 写 agent_working（含 slot）
    
    Returns: (session_id, operation_used)
    """
```

### Manager 场景

```
freely start:
  → acp_session_connect(__manager__, manager, manager_01, opencode-apikey-ds-flash-auto)
    → agent_working 有记录 + slot 匹配 → session/resume (缓存命中!)
    → agent_working 无记录 → session/new

freely restart (slot 变了):
  → acp_session_connect(__manager__, manager, manager_01, claude-apikey-ds-pro-auto)
    → agent_working 有记录 + slot 不匹配 → session/new (安全，不会报错)
```

### Worker 场景

```
watchdog 检测到需要 worker:
  → acp_session_connect(raw_key, worker, worker_01, opencode-apikey-ds-flash, message=task)
    → 有 session + slot 匹配 + alive → session/prompt (最快)
    → 有 session + slot 匹配 + dead → session/resume → prompt
    → 无 session + 同 tool → session/fork from Manager (缓存命中)
    → 无 session + 跨 tool → session/new
```

### Reviewer 场景

```
watchdog 检测到需要 reviewer:
  → acp_session_connect(raw_key, reviewer, reviewer_01, opencode-apikey-ds-flash, message=review_task)
    → 同 Worker 逻辑
    → 注意: gate review 用 session/new（不 fork，保持中立）
```

### 需要存储 slot 信息

`agent_working` 表需要新增 `slot` 列，session 创建/更新时写入：

```sql
ALTER TABLE agent_working ADD COLUMN slot TEXT DEFAULT '';
```

存储格式: `opencode-apikey-ds-flash-auto`（完整 slot 名）

### 需要的方法

| 方法 | 职责 |
|------|------|
| `acp_session_connect(project, raw_key, role, agent_id, slot, message)` | 统一入口，内部决策 new/fork/resume/prompt |
| `acp_session_register(project, raw_key, role, agent_id, session_id, slot, ...)` | 写入 agent_working（含 slot） |
| `acp_session_close(project, raw_key, role, agent_id)` | 清理 session_id |
| `acp_session_check_slot(project, raw_key, role)` | 检查存储的 slot 与当前是否一致 |

### 附：命名修正

`CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`（3 文件 11 处）

## Decision: 统一方法 `acp_session_connect`

核心抽象：**一个方法，根据 context 自动选择最优 session 操作**。

优先级: prompt > resume > fork > new
- prompt: alive session，零延迟
- resume: dead session 复活，保留上下文
- fork: 从 Manager 继承，缓存命中
- new: 最后手段，冷启动

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
