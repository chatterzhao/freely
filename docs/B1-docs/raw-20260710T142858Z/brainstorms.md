---
b1_id: B1-20260710T142858Z
phase_state: completed
source_raw: raw-20260710T142858Z
source_url: https://github.com/chatterzhao/freely/issues/3874
produced_candidate: C-20260710T142858Z-A
created_at: 2026-07-10
---

# B1_IBM: Runtime Worker Launch 接入 A2A

## Input

raw #3874: Manager 通过 a2a-exit 委派 Worker 后，A2A Task 停留在 submitted 状态，Worker ACP session 从未启动。

## Problem

### 观察证据

A2A tasks 表中有 4 个 `state=submitted, agent=worker` 的任务（raw_key=20260616T023944Z），最早的是 ~10 小时前创建的。所有都在 submitted 状态，没有一个进入 working。Worker bridge（opencode）处于 idle 状态，从未收到 session/prompt。

### 设计 vs 实现对比

`docs/system/workspace/a2a/acp-a2a-architecture.md` 定义了正确的全链路：

```
Manager → a2a-exit → A2A Task.message
Runtime → tasks/list → message→prompt file → Worker ACP session (fork)
Worker → work → a2a-exit completed → SSE → Manager 感知
```

| 步骤 | 设计 | 实现 | 状态 |
|------|------|------|:--:|
| Manager 委派 | a2a-exit --state submitted | `a2a-exit` tool → A2A Task | ✅ |
| A2A Task 存储 | POST /tasks → SQLite | A2A Server TaskStore | ✅ |
| Runtime 查询 | tasks/list --state=submitted | **未实现** | ❌ |
| message→prompt | Task.message → 临时 prompt file | **未实现** | ❌ |
| Worker ACP 启动 | session/fork from Manager | **未实现** | ❌ |
| Worker 完成通知 | a2a-exit completed → SSE | SSE 已就绪 | ⚪ |

### 根因

`manager_runtime_launch_workers_from_latest_task()` (line 13297) 只处理旧的 **continuity 文件 + CSV prompt 列表** 系统，从未查询 `a2a_tasks` 表。

旧系统（CSV 时代）:
```
Manager → 写 continuity 文件 → CSV prompt 列表 → Runtime 读 CSV → 启动 Worker
```

新系统（A2A 时代，设计已就绪但未接入）:
```
Manager → a2a-exit → A2A Task → Runtime 查 tasks/list → 启动 Worker
```

两个系统并行存在，但 Runtime 的 Worker launch 只接在旧管道上。A2A 管道建好了但没有水。

### 影响范围

不只是 Worker launch——整个 agent 协作链路的其他环节也可能有同样问题：

| 功能 | 新系统状态 | 旧系统状态 |
|------|----------|----------|
| Manager 委派 Worker | A2A Task (新) ✅ | continuity file (旧) ⚪ |
| Worker 启动 | **未接入 A2A** ❌ | continuity file (旧) ✅ |
| Worker 状态上报 | a2a-exit completed (新) ✅ | — |
| Manager 感知 Worker 完成 | SSE (新) ✅ | 轮询 (旧) ⚪ |
| Reviewer 触发 | A2A SSE → watchdog → ACP | watchdog 已就绪但无 Worker 输出 |
| Agent Card 暴露 | agent-roles.toml → AgentCard | — |

## Discovery

### 价值判断

**P0 阻塞问题。** Worker 不启动 = Manager 的所有委派都是空转 = Freely 的核心价值（AI 自主开发）无法实现。

### 提交历史分析

A2A 集成分为三个阶段，当前停在 Phase 2 和 Phase 3 之间：

**Phase 1 (6月中旬): A2A Server + TaskStore**
- A2A Server 实现 (a2a_server.py, TaskStore on SQLite)
- Agent Card 端点 (/.well-known/agent-card.json)
- SSE 全局流端点 (GET /tasks/stream)
- a2a_task.py CLI 客户端

**Phase 2 (6月下旬-7月初): Manager 侧 A2A 集成**
- `a2a-exit` tool → Manager 用 A2A 协议委派 ✅
- agent-roles.toml (替代旧 roles.toml) ✅
- watchdog_sse.py (SSE 监听 + Reviewer 触发) ✅
- `_restore_tasks()` (A2A Server 启动时状态恢复) ✅

**Phase 3 (未完成): Runtime 侧 A2A 集成**
- ❌ `manager_runtime_launch_workers_from_latest_task()` 接入 A2A
- ❌ A2A Task.message → prompt file → Worker ACP session
- ❌ Worker launch 后更新 task state (submitted → working)

## Brainstorm

### Option A: 最小接入（推荐）
在 `manager_runtime_launch_workers_from_latest_task()` 中增加 A2A 查询路径：
1. `tasks/list --state=submitted --role=worker` → 获取待处理任务列表
2. 对每个 task: 从 `message` 字段生成临时 prompt file
3. 调用现有 `launch_worker_from_manager_prompt_if_needed()` 启动 Worker
4. Worker 启动后更新 task state: `submitted → working`
5. 保留旧 continuity 系统作为 fallback

### Option B: 完全替换为 A2A
移除所有 continuity/CSV 相关代码，只使用 A2A 路径。

**缺点**: 风险大，continuity 系统还承载 handoff/context rotation 等功能。

### Option C: 新函数 + 双路径
新建 `manager_runtime_launch_workers_from_a2a_tasks()` 函数，与旧函数并行调用。

**缺点**: 增加代码重复，维护两个平行的 Worker launch 路径。

## Decision: Option A

1. `manager_runtime_launch_workers_from_latest_task()` 增加 A2A tasks 查询
2. 复用现有 `launch_worker_from_manager_prompt_if_needed()` 
3. 旧 continuity 路径保留作为 fallback
4. A2A task state 在 Worker 启动/完成时正确更新

## 额外需要审查
- Worker ACP session 启动后是否正确使用 session/fork（继承 Manager 治理上下文）
- Worker 完成后 a2a-exit completed 是否正确触发 SSE 通知
- Reviewer 的 watchdog_sse 是否能正确收到 Worker 完成的 SSE 事件并触发审查

## Candidate
- candidate_id: C-20260710T142858Z-A
- status: promoted
- milestone: M-20260710T142858Z-A
