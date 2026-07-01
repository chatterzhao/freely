---
b1_id: B1-20260701T085407Z
phase_state: completed
source_raw: raw-20260701T085407Z
source_url: https://github.com/chatterzhao/freely/issues/3697
produced_candidate: C-20260701T085407Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A reviewer agent — 现状 vs 目标架构

## 1. 当前架构（问题版）

```
┌─Runtime (轮询编排)────┐  ┌─a2a_tasks (SQLite)──┐  ┌─1 个 A2A Server──┐  ┌─ACP Bridge─────────┐  ┌─Agents────────────┐
│                       │  │                     │  │                   │  │                    │  │                   │
│ 启动 DB/A2A/ACP       │  │                     │  │ agent card:       │  │ 1 process:         │  │                   │
│                       │  │                     │  │ "Freely Worker"   │  │ claude-agent-acp   │  │                   │
│                       │  │                     │  │ (所有角色共用)     │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│──poll────────────────▶│  │                     │  │                   │  │                    │  │                   │
│  a2a_task.py list     │  │                     │  │                   │  │                    │  │                   │
│  每 N 秒轮询 state    │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│ 发现 scan item        │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│──写 prompt 文件──────▶│  │                     │  │                   │  │                    │  │                   │
│  (文件方式委派worker)  │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│──start_workcell──────▶│  │                     │  │                   │  │                    │  │                   │
│  启动 worker daemon   │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │──ACP fresh────────▶│──Manager (develop)─│
│                       │  │                     │  │                   │  │  1 session         │  patrol scan       │
│                       │  │                     │  │                   │  │                    │  │                   │
│                       │  │◀──a2a_store write───│  │                   │  │                    │──Worker (fix wt)───│
│                       │  │  state=working      │  │                   │  │                    │  │  B1 skill         │
│                       │  │                     │  │                   │  │                    │  │                   │
│                       │  │◀──a2a_store write───│  │                   │  │                    │  │  state=input      │
│                       │  │  state=input-required│ │                   │  │                    │  │  -required        │
│                       │  │                     │  │                   │  │                    │  │                   │
│──poll────────────────▶│  │                     │  │                   │  │                    │  │                   │
│  detect input-required│  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│  freely-cycle 建议:   │  │                     │  │                   │  │                    │  │                   │
│  dispatch_reviewer    │  │                     │  │                   │  │                    │  │                   │
│  ❌ 但无人执行         │  │                     │  │                   │  │                    │  │                   │
│                       │  │                     │  │                   │  │                    │  │                   │
│ 🔴 Reviewer 不存在     │  │                     │  │ 🔴 SSE 端点存在     │  │                    │  │                   │
│ 🔴 没有 agent card     │  │                     │  │    但无人订阅       │  │                    │  │                   │
│ 🔴 没有 ACP session    │  │                     │  │                    │  │                    │  │                   │
│                       │  │                     │  │                    │  │                    │  │                   │
│                       │  │                     │  │                    │  │                    │  │                   │
│ 🔴 全部问题:           │  │                     │  │                    │  │                    │  │                   │
│ 1. 轮询代替 SSE        │  │                     │  │                    │  │                    │  │                   │
│ 2. 1 个 card 代替 3 个 │  │                     │  │                    │  │                    │  │                   │
│ 3. prompt 文件代替 A2A │  │                     │  │                    │  │                    │  │                   │
│ 4. Reviewer 不存在     │  │                     │  │                    │  │                    │  │                   │
│ 5. _restore_tasks 有   │  │                     │  │                    │  │                    │  │                   │
│    and/or 优先级 bug   │  │                     │  │                    │  │                    │  │                   │
└───────────────────────┘  └─────────────────────┘  └───────────────────┘  └────────────────────┘  └───────────────────┘
```

### 当前 5 个问题

| # | 问题 | 影响 |
|---|------|------|
| 1 | Runtime **轮询** a2a_tasks，不用 SSE | 延迟高，实时性差 |
| 2 | 只有 **1 个 agent card** "Freely Worker" | Manager/Reviewer 无独立身份 |
| 3 | Worker 委派用 **prompt 文件** 不用 A2A task | 无法追踪、恢复、SSE 推送 |
| 4 | **Reviewer 不存在** — 无 card、无 session、无 task | 完全缺失 |
| 5 | a2a_server.py `_restore_tasks()` **and/or 优先级 bug** | Reviewer 误入 Worker 恢复逻辑 |


## 2. 目标架构（正确设计）

基于 A2A/ACP 协议最佳实践 + Zed 参考实现：

```
┌─Runtime (A2A Orchestrator)─────────────────────────────────────────────────────────────────────┐
│                                                                                                │
│  职责: 启动 ACP connections, 创建 A2A tasks, 订阅 SSE, 路由 state changes                       │
│                                                                                                │
│  ┌─ACP Bridge (1 process, 多 session)──────────────────────────────────────────────────────┐   │
│  │  claude-agent-acp                                                                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                                  │   │
│  │  │Session: Mgr  │  │Session: Rev  │  │Session: Wrk  │                                  │   │
│  │  │conversation  │  │conversation  │  │conversation  │                                  │   │
│  │  │_id: mgr-01   │  │_id: rev-m-01 │  │_id: wrk-01   │                                  │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                                  │   │
│  └─────────┼─────────────────┼─────────────────┼──────────────────────────────────────────┘   │
│            │                 │                 │                                               │
│  ┌─────────┼─────────────────┼─────────────────┼──────────────────────────────────────────┐   │
│  │         │          A2A Server (per-role agent cards)                                    │   │
│  │         │                                                                               │   │
│  │  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐                                  │   │
│  │  │Manager Card  │  │Reviewer Card │  │Worker Card   │                                  │   │
│  │  │skills:       │  │skills:       │  │skills:       │                                  │   │
│  │  │ patrol       │  │ tdd-review   │  │ B1, B2       │                                  │   │
│  │  │ delegate     │  │ code-review  │  │ RED, dev     │                                  │   │
│  │  │ wt-create    │  │ gate-check   │  │ test, GREEN   │                                  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                                  │   │
│  └────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                │
│                                      │                                                         │
│                              a2a_tasks (SQLite)                                                │
│                        ┌─────────────────────────┐                                             │
│                        │ a2a_store: agent 读写    │                                             │
│                        │ a2a_sse:   实时推送      │                                             │
│                        │   GET /tasks/{id}/stream │                                             │
│                        └────────┬────────────────┘                                             │
│                                 │                                                              │
│              ┌──────────────────┼──────────────────┐                                           │
│              │                  │                  │                                           │
│              ▼                  ▼                  ▼                                           │
│        Manager             Reviewer            Worker                                         │
│        (develop)           (develop)           (fix wt)                                        │
│        订阅 worker SSE     订阅被委派 task      执行 skill                                      │
│        委派 reviewer       审查 + 输出 guidance  state=input-required                          │
│                            SSE 推送 verdict     等待 reviewer guidance                         │
│                                                                                                │
└────────────────────────────────────────────────────────────────────────────────────────────────┘

时序:

  Runtime       ACP        a2a_tasks    Manager      Worker      Reviewer
    │            │             │           │            │            │
    │──ACP fresh─────────────▶│           │            │            │
    │  Session: Manager       │           │            │            │
    │            │             │           │            │            │
    │──A2A task:manager──────▶│           │            │            │
    │  state=submitted        │           │            │            │
    │            │             │           │            │            │
    │            │             │           │──patrol──▶│            │
    │            │             │           │            │            │
    │            │             │           │──delegate─────────────▶│
    │            │             │           │  A2A task:worker       │
    │            │             │           │  state=submitted       │
    │            │             │           │            │            │
    │──ACP fork──────────────▶│           │            │            │
    │  Session: Worker        │           │            │            │
    │            │             │           │            │──B1────▶  │
    │            │             │           │            │  working  │
    │            │             │◀──a2a_store write──────│            │
    │            │             │  state=input-required  │            │
    │            │             │           │            │            │
    │            │             │──a2a_sse push─────────▶│            │
    │            │             │  notify: input-required│            │
    │            │             │           │            │            │
    │            │             │           │──dispatch────────────────▶│
    │            │             │           │  A2A task:reviewer       │
    │            │             │           │            │            │
    │──ACP fresh─────────────▶│           │            │            │
    │  Session: Reviewer      │           │            │            │
    │            │             │           │            │──review──▶│
    │            │             │           │            │  working  │
    │            │             │◀──a2a_store write───────────────────│
    │            │             │  state=completed, verdict=pass      │
    │            │             │           │            │            │
    │            │             │──a2a_sse push─────────▶│            │
    │            │             │  notify: reviewer done │            │
    │            │             │           │            │            │
    │            │             │           │──route────────────────▶│
    │            │             │           │  continue: B2          │
    │            │             │           │            │            │
```

## 3. Agent Role Card 设计

### 文件布局

```
.freely/agent-table.toml                    ← untracked, 用户配置 (slot)
docs/system/workspace/agents/               ← git tracked, 定义角色能力
├── manager.card.toml                         (Manager 能做什么)
├── worker.card.toml                          (Worker 能做什么)
└── reviewer.card.toml                        (Reviewer 能做什么)
```

### 职责分离

| 文件 | 位置 | Git | 谁维护 | 内容 |
|------|------|:--:|------|------|
| agent-table.toml | .freely/ | ❌ | 用户 (freely init) | slot, reviewer配对, pool |
| manager.card.toml | docs/system/workspace/agents/ | ✅ | 开发者 (代码) | skills, capabilities |
| worker.card.toml | docs/system/workspace/agents/ | ✅ | 开发者 (代码) | skills, capabilities |
| reviewer.card.toml | docs/system/workspace/agents/ | ✅ | 开发者 (代码) | skills, capabilities |

### card.toml 示例（纯能力声明，不提 slot）

```toml
# docs/system/workspace/agents/manager.card.toml
[agent]
name = "Freely Manager"
description = "Patrol fleet, delegate workers, judge closeout"

[[skills]]
id = "freely-workflow-guarded-execution"
name = "Patrol & Delegate"
tags = ["manager"]

[[skills]]
id = "freely-branch-management"
name = "Branch Management"
tags = ["manager"]
```

```toml
# docs/system/workspace/agents/worker.card.toml
[agent]
name = "Freely Worker"
description = "Worktree-isolated, skill-based execution"

[[skills]]
id = "freely-doc-B1_IBM-execution"
name = "B1 Pre-Research"
tags = ["worker"]

[[skills]]
id = "freely-doc-B2_IBM-execution"
name = "B2 Design"
tags = ["worker"]

[[skills]]
id = "freely-test-RED-execution"
name = "RED Phase"
tags = ["worker"]

[[skills]]
id = "freely-dev-loop-execution"
name = "Dev Implementation"
tags = ["worker"]

[[skills]]
id = "freely-test-execution"
name = "GREEN Phase"
tags = ["worker"]
```

```toml
# docs/system/workspace/agents/reviewer.card.toml
[agent]
name = "Freely Reviewer"
description = "Per-step review, gate check, TDD fidelity"

[[skills]]
id = "freely-tdd-review"
name = "TDD Fidelity Review"
tags = ["reviewer"]

[[skills]]
id = "freely-candidate-acceptance-review"
name = "Candidate Acceptance Review"
tags = ["reviewer"]
```

### slot 与 card 的绑定：Runtime + ACP 层面

```
agent-table.toml          role.card.toml           ACP session 创建时
─────────────────         ─────────────            ─────────────────
manager_slot=claude   +   Manager card skills  →   acp-bridge.py start
                          (纯能力声明)              --slot claude-apikey-ds-pro
                                                   --role manager
                                                   
worker_slot=claude    +   Worker card skills    →   acp-bridge.py start  
                                                   --slot claude-apikey-ds-pro
                                                   --role worker

reviewer slot 继承     +   Reviewer card skills  →   acp-bridge.py start
自 parent 的 slot                                   --slot <same as parent>
                                                    --role reviewer
```

**关键**：card 永远不提 slot。slot 是 Runtime 从 agent-table 读取后，在创建 ACP session 时作为参数传入。

## 4. 重构 TODO List

### Phase A: A2A Server — 多 agent card
- [ ] 每个 agent 角色生成独立 agent card（Manager/Worker/Reviewer）
- [ ] agent card 从 agent-table.toml 读取身份信息
- [ ] `/.well-known/agent-card.json` 按 role 参数返回对应 card
- [ ] agent card skills 按角色区分（Manager: patrol/delegate, Worker: B1/B2/dev, Reviewer: review）

### Phase B: _restore_tasks — reviewer 恢复路径
- [ ] 修 L403/442/663 的 and/or 优先级（加括号）
- [ ] 新增 `state=working + reviewer前缀` → ACP session 存活检查
- [ ] 新增 `state=input-required + reviewer前缀` → worker task 依赖检查

### Phase C: Runtime — SSE 订阅替代轮询
- [ ] Runtime 订阅 A2A SSE 端点（`GET /tasks/{id}/stream`）
- [ ] 收到 `input-required` SSE 推送 → 路由到对应 handler
- [ ] 轮询保留为 fallback（SSE 断连时）
- [ ] freely-cycle 从"建议 dispatch_reviewer" 改为 "实际创建 reviewer A2A task"

### Phase D: Agent 委派 — A2A task 替代 prompt 文件
- [ ] Manager 委派 Worker: `POST /tasks` 创建 A2A task（替代 prompt 文件）
- [ ] Manager 委派 Reviewer: `POST /tasks` 创建 reviewer task
- [ ] Worker 状态变更: `PATCH /tasks/{id}` → a2a_store → SSE push
- [ ] Reviewer 审查结论: `PATCH /tasks/{id}` → verdict 写入 message 字段

### Phase E: ACP session 管理
- [ ] `_ensure_reviewer_agent()`: 接受 reviewer_id 参数，创建 ACP session
- [ ] ACP session 命名: `{role}_{id}` (manager_01, reviewer_worker_01, worker_03)
- [ ] Session fork 用于 worker（从 develop fork 到 fix worktree）
- [ ] Session resume 用于恢复（daemon 重启后）

## Candidate

- candidate_id: C-20260701T085407Z-A
- status: promoted
- milestone: M-20260701T085407Z-A
- promoted_issue_id: I-20260701T085407Z-A
- decision_reason: 基于 A2A/ACP 协议最佳实践 + Zed 参考，5 阶段渐进重构
- next_action: B2 设计 → 逐 Phase 实现 → PR

## 5. ACP vs A2A — 职责边界

### 一句话

```
ACP = agent ↔ AI     (垂直：给 agent 装上大脑)
A2A = agent ↔ agent  (水平：agent 之间协作)
```

### 对比

| 维度 | ACP | A2A |
|------|-----|-----|
| **通信方向** | Client → AI CLI tool | Agent ↔ Agent |
| **谁用** | Runtime 给 agent 创建 session | Agent 之间委派任务 |
| **传输** | JSON-RPC over stdio | HTTP + SSE over Unix socket |
| **核心概念** | session, conversation_id, fork/resume | task, agent card, state machine |
| **状态管理** | 会话上下文 (对话历史) | 任务状态 (submitted→working→completed) |
| **实时推送** | 无 (同步 RPC) | SSE (状态变更实时通知) |
| **谁启动** | Runtime 启动 acp-bridge.py | Runtime 启动 a2a_server.py |
| **配置来源** | agent-table.toml (slot) | role.card.toml (skills) |

### 在 Freely 中的具体场景

```
场景                          用哪个      具体操作
──────────────────────────    ────       ──────────────────────────────
Runtime 给 Manager 装大脑      ACP        acp-bridge.py → session/new
                                          prompt: "你是 Manager, 巡逻..."

Manager 委派 Worker 做 B1     A2A        POST /tasks {role:worker, skill:B1}
                                          state: submitted → working

Worker 报告 B1 完成            A2A        PATCH /tasks/{id} state=input-required
                                          → A2A SSE push → Manager 收到

Manager 委派 Reviewer 审查     A2A        POST /tasks {role:reviewer, skill:tdd-review}

Runtime 给 Reviewer 装大脑     ACP        acp-bridge.py → session/new
                                          prompt: "审查 B1 产物..."

Reviewer 输出审查结论          A2A        PATCH /tasks/{id} state=completed
                                          message: {verdict:pass, guidance:"..."}
                                          → A2A SSE push → Manager 收到

Manager 让 Worker 继续 B2     A2A        POST /tasks {role:worker, skill:B2}
                                          (附带 reviewer guidance)

Daemon 重启，恢复 Manager     ACP        session/resume (从 session-store)
                                          或 session/new (无历史时)

Daemon 重启，恢复未完成 task   A2A        _restore_tasks() 读 SQLite
                                          检查 worker/reviewer 存活状态
```

### 关键认知

```
ACP 不关心 agent 之间怎么协作 —— 它只管"这个 agent 能不能调用 AI"
A2A 不关心 agent 用哪个 AI  —— 它只管"agent 之间怎么发现、委派、同步状态"

两者正交：
  - 同一个 ACP process 可以服务 Manager + Reviewer (不同 session)
  - 同一个 A2A task 可以经历多个 ACP session (daemon 重启后 resume)
  - Agent card (A2A) 声明"我能做什么"，agent-table (ACP 配置) 声明"我用什么做"
```

### 当前实现偏差

```
场景                          应该用      当前实际用      问题
──────────────────────────    ────       ──────────      ──────────────────
Manager 委派 Worker           A2A task   prompt 文件      无状态追踪，无 SSE
Worker 报告完成                A2A SSE    a2a_task.py 轮询 延迟高，实时性差
Reviewer 不存在                A2A+ACP    无              完全缺失
Agent 身份                    3 card     1 card "Worker"  Manager/Reviewer 无独立 card
```

