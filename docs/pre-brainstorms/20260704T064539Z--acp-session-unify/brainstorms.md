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

### 全局理解

Freely 的 agent 通信模型：agent-table 配置 slot → daemon 启动 ACP bridge → 各 agent 创建/恢复 session → A2A SSE 事件驱动 agent 间通信 → session/prompt 实现 agent 间消息传递。

四种 ACP session 操作：

| 操作 | 用途 | 缓存 | 约束 |
|------|------|:---:|------|
| `session/new` | 全新开始、slot 变更、跨 tool | ❌ | 无约束 |
| `session/fork` | 从父 session 继承 context | ✅ | **同 tool 才行**，跨 tool 报错 |
| `session/resume` | 恢复不活跃 session | ✅ | **slot 必须没变**，否则报错 |
| `session/prompt` | 向 alive session 发消息 | N/A | session 必须 alive |

### 每个 agent 都需要 resume

Manager 不是唯一需要 resume 的。Worker 和 Reviewer 也会因为 idle timeout 导致 session 不活跃，需要 resume 恢复。当前 watchdog_sse.py 已部分处理（`_handle_needs_worker` line 469-477: 先查 alive session → prompt，失败则 fork/new），但缺少 resume 尝试——如果 session 存在但 dead，应优先 resume 而非直接 new。

### Reviewer 的独立性

Workflow skill 明确：**每个节点后都需要独立 review**。三个 loop 的设计保证了每个环节都有 review gate。

Reviewer **必须 fork Manager，不能 fork Worker**：
- fork Manager → 继承 governance context (CONSTITUTION, LAWS, project map)，不知道 Worker 的思考过程 → 独立公正
- fork Worker → 看到 Worker 的实现细节和思考 → 自评自审，失去 review 意义
- 如果没有 review → 实现会糊弄完成 → loop 的设计就是为了保证每个环节都独立验证

### 当前差距

**1. 无统一 session 操作选择方法。** 决策逻辑散落在 watchdog_sse.py 和 freely shell。

**2. agent_working 无 slot 列。** 无法判断 session 创建时的 slot 是否与当前一致。Manager 每次重启都 session/new，不敢 resume（怕 slot 变了报错）。

**3. Worker/Reviewer 的 resume 路径不完整。** watchdog 有 alive check 和 fork/new，但缺少"dead → resume"的尝试。

## Brainstorm

### 统一方法：acp_session_connect

```
acp_session_connect(project, raw_key, role, agent_id, slot, message=None)
  → (session_id, operation_used)

决策树（按优先级）:
  1. agent_working 有 session_id?
     ├─ 有 + slot 匹配
     │   ├─ alive?      → session/prompt(message)     【最快: 0ms】
     │   └─ dead?       → session/resume → prompt     【恢复: 保留上下文】
     └─ 有 + slot 不匹配 → session/new                【安全: 不会报错】
  2. 无 session_id
     ├─ 同 tool + role≠reviewer_gate → session/fork(Mgr)  【缓存命中: 继承治理】
     └─ 否则                        → session/new          【兜底: 冷启动】
  3. 成功 → 写 agent_working (含 slot)
```

### 三个角色的 session 策略

| | 首次 | 重启/恢复 | 同 tool fork | 跨 tool | session/prompt |
|------|------|------|:---:|:---:|:---:|
| Manager | new | **resume** (需 slot 匹配) | N/A | new | N/A |
| Worker | fork(Mgr) | prompt / **resume** / new | fork(Mgr) | new | Manager→Worker |
| Reviewer | fork(Mgr) | prompt / **resume** / new | fork(Mgr) | new | Worker→Reviewer, Reviewer→Worker |

**Reviewer fork 策略：**
- 正常 review：fork Manager（继承治理 context，不知道 Worker 思考 → 独立公正）
- Gate review：session/new（最大独立性，冷启动无偏见）
- **永不 fork Worker**（自评自审 = 作弊）

### 需要存储 slot

`agent_working` 新增 `slot` 列：

```sql
ALTER TABLE agent_working ADD COLUMN slot TEXT DEFAULT '';
```

session 创建/更新时写入完整 slot 名（如 `opencode-apikey-ds-flash-auto`），恢复时比对。

### 需要的方法

| 方法 | 职责 |
|------|------|
| `acp_session_connect()` | 统一入口，内部决策 prompt/resume/fork/new |
| `acp_session_register()` | 写入 agent_working（含 slot） |
| `acp_session_close()` | 清理 session_id |
| `acp_session_can_resume()` | 检查 slot 是否匹配，能否安全 resume |

### 附：命名修正

`CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`（3 文件 11 处）

## Decision

核心交付：
1. `acp_session_connect()` — 统一 session 操作选择
2. agent_working 加 `slot` 列 — 安全 resume 的前提
3. 三个角色都走同一方法 — prompt>resume>fork>new 优先级
4. Reviewer 永远 fork Manager（独立），不 fork Worker（作弊）
5. 命名修正

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
