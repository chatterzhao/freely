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


## 6. Runtime Watchdog + Agent 直连 A2A SSE

### 核心原则

```
Runtime 不是中间人，是启动者。

  Runtime Watchdog           Agent ↔ Agent
  ────────────────           ─────────────
  监听 SSE                   直连 A2A SSE
  检测"需要新 agent"信号      互相推送 task state
  ACP 创建 session           不需要 Runtime 中转
  然后退到后台继续监听        自己对话
```

### 完整时序

```
Runtime Watchdog     ACP            a2a_tasks       Worker           Reviewer
(SSE listener)      (session factory)              (fix wt)         (develop)
     │                 │                │             │                 │
     │                 │                │──B1 done───▶│                 │
     │                 │                │ state=      │                 │
     │                 │                │ input-required               │
     │                 │                │             │                 │
     │◀──A2A SSE push──│                │             │                 │
     │  detect:        │                │             │                 │
     │  worker needs   │                │             │                 │
     │  review         │                │             │                 │
     │                 │                │             │                 │
     │──ACP session/new▶               │             │                 │
     │  role=reviewer  │                │             │                 │
     │  paired=worker  │                │             │                 │
     │                 │                │             │                 │
     │                 │──Reviewer boots─────────────▶│                 │
     │                 │                │             │                 │
     │ (退到后台)       │                │             │                 │
     │                 │                │             │                 │
     │                 │                │◀──A2A SSE────────────────────│
     │                 │                │  "开始审查 B1 产物"           │
     │                 │                │             │                 │
     │                 │                │──A2A SSE───▶│                 │
     │                 │                │  "审查中..."  │                 │
     │                 │                │             │                 │
     │                 │                │◀──A2A SSE────────────────────│
     │                 │                │  state=completed             │
     │                 │                │  verdict=pass                │
     │                 │                │  guidance="没有问题，继续推进" │
     │                 │                │             │                 │
     │                 │                │──A2A SSE───▶│                 │
     │                 │                │  "reviewer:│                 │
     │                 │                │   pass,     │                 │
     │                 │                │   继续 B2"  │                 │
     │                 │                │             │                 │
     │                 │                │             │──B2 skill────▶  │
     │                 │                │             │                 │
     │ (Runtime 不需要介入这步)          │             │                 │
```

### Runtime 介入 vs 不介入

```
Runtime 介入 (ACP session/new):           Runtime 不介入 (Agent 直连 A2A SSE):
──────────────────────────────           ──────────────────────────────
• Worker 第一次需要 Reviewer              • Worker 报告进度给 Reviewer
• Reviewer 还没启动                       • Reviewer 推送 verdict 给 Worker  
• Agent crash 需重新启动                  • 正常的 task state 变更
• Daemon 重启需恢复 agent                 • "working", "completed" 等状态更新
```

### 三个 agent 的 A2A SSE 订阅关系

```
                    a2a_tasks
                   ┌─────────┐
                   │  SSE    │
                   │  Push   │
                   └──┬──┬───┘
                      │  │
         ┌────────────┼──┼────────────┐
         │            │  │            │
         ▼            ▼  ▼            ▼
     Manager       Worker         Reviewer
   (develop)      (fix wt)       (develop)
       │              │               │
       │ 订阅:         │ 订阅:          │ 订阅:
       │ 所有 worker   │ 自己 task      │ 自己被委派
       │ 所有 reviewer │ 的配对 reviewer│ 的 task
       │ 的 state 变更 │ 的 verdict     │
       │              │               │
       └──────────────┴───────────────┘
         Runtime Watchdog 额外订阅:
         所有 input-required → 判断是否需创建新 agent
```


## 7. input-required 路由：不是一种，是多种

### input-required 类型与处理方式

```
Worker 发出 state=input-required
         reason={type}

┌─────────────────────────────────────────────────────────────────────┐
│ reason                         谁处理          ACP 动作             │
├─────────────────────────────────────────────────────────────────────┤
│ needs-human-input              Manager        session/resume       │
│   worker 需要人回答一个问题      (已有 session)  prompt: "worker 问:..." │
│                                 Manager 通过 ACP prompt 问人         │
│                                 人回答后 Manager 通过 ACP 回复 worker │
├─────────────────────────────────────────────────────────────────────┤
│ needs-review:b1                 Reviewer       session/fork (同 tool)│
│   B1 完成，需审查是否达标        (不存在!)      session/new  (跨 tool) │
│                                                Reviewer 审查 B1 产物  │
│                                                verdict: pass → B2    │
│                                                verdict: redo → 重做 B1│
├─────────────────────────────────────────────────────────────────────┤
│ needs-review:b2                 Reviewer       同上                  │
│   B2 设计完成，需审查设计质量    (可能存在)     如果已存在 → 复用 sess │
│                                 (同 worker 配对) verdict: pass → RED  │
├─────────────────────────────────────────────────────────────────────┤
│ needs-review:dev                Reviewer       同上                  │
│   代码实现完成，需 TDD 审查      (可能存在)     verdict: pass → test   │
├─────────────────────────────────────────────────────────────────────┤
│ needs-manager-decision          Manager         session/resume       │
│   遇到阻塞/冲突/需决策           (已有 session)  Manager 判断:         │
│                                                merge? close?         │
│                                                re-delegate? stop?    │
└─────────────────────────────────────────────────────────────────────┘
```

### Reviewer 启动策略

```
Reviewer 是否存在?    用什么 ACP 动作          原因
──────────────────   ────────────────────     ──────────────────────
首次需要 Reviewer     session/new             没有可复用的 session
同 tool (claude)     session/fork (from Mgr)  复用连接，轻量启动
跨 tool (codex)      session/new              不同 binary，必须新建
上次 crash 后恢复     session/resume           从 session-store 恢复
已存在且空闲         直接 A2A SSE 推送 task    最快，零启动
```

### 完整 B1 场景示例

```
Worker: 完成 B1 brainstorms + candidate
        → a2a_store: state=input-required, reason=needs-review:b1
        → a2a_sse: push to subscribers

Runtime Watchdog:
  收到 SSE: {worker=wrk-01, state=input-required, reason=needs-review:b1}
  → 判断: 需要 Reviewer，且 reviewer_worker_01 不存在
  → ACP: session/fork (同 tool=claude, 从 Manager session fork)
  → 启动 Reviewer agent: "审查 worker wrk-01 的 B1 产物"

Reviewer (ACP session 启动后):
  → 读取 Worker 的 B1 产物 (brainstorms.md, candidates.md)
  → 按 skill:freely-tdd-review 四层审查
  → 结论:
    Option A: "B1 达标，可以进入 B2"
      → a2a_store: state=completed, verdict=pass, guidance="继续 B2"
      → a2a_sse push → Worker 收到
    Option B: "B1 不达标，根因分析不充分"
      → a2a_store: state=completed, verdict=fail, guidance="重做根因分析"
      → a2a_sse push → Worker 收到 → 重做 B1
    Option C: "scope 太大，需 Manager 决策是否拆分"
      → a2a_store: state=completed, verdict=blocked, guidance="scope太大"
      → a2a_sse push → Manager 收到 → Manager 决策拆分/继续

Worker (收到 Reviewer verdict):
  pass    → 继续下一步 (B2 skill)
  fail    → 回到当前步重做
  blocked → 等待 Manager 决策
```


## 8. Agent 配对与工作交接机制

### 8a. input-required 是双向的，三向互指

```
任何 agent 都可以 needs-{另一个}:

Worker ──needs-reviewer──▶ Reviewer   (B1/B2/dev 完成后需审查)
Worker ──needs-manager───▶ Manager    (遇到阻塞/冲突/需决策)
Reviewer──needs-worker───▶ Worker     (审查不通过，需重做)
Reviewer──needs-manager──▶ Manager    (scope 问题需 Manager 决策)
Manager ──needs-reviewer──▶ Reviewer  (Manager 主动发起审查)
Manager ──needs-worker───▶ Worker     (Manager 委派新任务)
```

### 8b. ACP session 与 worktree 绑定

```
session/new  → 必须有 worktree，在 worktree 上工作
session/fork → 从父 session fork，继承 worktree
session/resume → 恢复，仍在原 worktree
session/close → wt-close 命令内封装，关闭 worktree 时同时关闭

规则:
  Manager:  worktree = develop (唯一)
  Worker:   worktree = fix/raw-{key}-{slug} 或 feature/raw-{key}-{slug}
  Reviewer: worktree = 其配对 Worker 的 test-pre-merge-{key}-{slug}
  
  session/close 时机: wt-close 命令内，先关 session 再删 worktree
```

### 8c. 多工位并发时的配对机制

**核心问题**: 10 个 worker 并发，10 个 reviewer，怎么保证 reviewer_worker_03 审查的是 worker_03 的产出？

**配对链条**:

```
agent-table.toml          agent-id.env                  worktree
─────────────────         ────────────                  ────────
worker_id = worker_01     fix/raw-KEY1-xxx=worker_01    fix/raw-KEY1-xxx
pool = 10                 fix/raw-KEY2-yyy=worker_02    fix/raw-KEY2-yyy
                          fix/raw-KEY3-zzz=worker_03    fix/raw-KEY3-zzz

配对规则: NN 对号 + raw-key 对齐 + worktree 绑定

worker_01 ←────────── 配对 ──────────→ reviewer_worker_01
   │                                       │
   │ worktree: fix/raw-KEY1-xxx            │ worktree: test-pre-merge-KEY1-xxx
   │ raw-key: KEY1                         │ raw-key: KEY1 (继承)
   │                                       │
   └── 同一个 raw-key ─────────────────────┘

worker_02 ←────────── 配对 ──────────→ reviewer_worker_02
   │                                       │
   │ worktree: fix/raw-KEY2-yyy            │ worktree: test-pre-merge-KEY2-yyy
   │ raw-key: KEY2                         │ raw-key: KEY2 (继承)
   │                                       │
   └── 同一个 raw-key ─────────────────────┘
```

**配对保证机制**:

```
创建时:
  1. wt-create 创建 fix/raw-{key}-{slug} + test-pre-merge-{key}-{slug}
  2. agent-id.env 记录: fix/raw-{key}-{slug}=worker_NN
  3. worker_NN 是 pool 中下一个可用编号 (01, 02, ...)
  4. reviewer_worker_NN 自动配对 (同 NN)

运行时:
  5. Worker 在 fix/raw-{key} 上工作
  6. Worker 设 needs-reviewer 时，A2A task 携带 raw-key 和 worker_NN
  7. Runtime Watchdog 检测到 → 创建 reviewer_worker_NN
  8. Reviewer 绑定到 test-pre-merge-{key} (同 raw-key 的 test 工位)
  9. Reviewer 通过 raw-key 找到 Worker 的产物 (docs/epics/.../raw-{key}/)

wt-close 时:
  10. wt-close fix/raw-{key} → 先 session/close worker_NN
  11. → session/close reviewer_worker_NN (如果存在)
  12. → 删除 test-pre-merge-{key} worktree
  13. → 删除 fix/raw-{key} worktree
  14. agent-id.env 清理: 移除 fix/raw-{key} 的绑定
```

### 8d. A2A task 中的配对字段

```
A2A task 创建时携带配对信息:

{
  "task_id": "uuid",
  "agent_id": "reviewer_worker_03",     ← 谁处理
  "role": "reviewer",
  "raw_key": "20260701T085407Z",        ← 哪个 issue
  "worktree": "test-pre-merge-20260701T085407Z-xxx",  ← 在哪个工位
  "parent_agent": "worker_03",          ← 配对的 worker
  "parent_worktree": "fix/raw-20260701T085407Z-xxx",  ← worker 的工位
  "skill": "freely-tdd-review",
  "state": "submitted"
}
```

配对字段确保:
- `raw_key`: Reviewer 能找到 Worker 的产物
- `parent_agent`: 知道是谁发起的审查请求
- `worktree` + `parent_worktree`: 同一 raw-key 的 dev↔test 工位对

### 8e. 并发安全

```
场景: 10 个 Worker 同时 needs-reviewer

worker_01 needs-reviewer → Runtime Watchdog 检测 → 创建 reviewer_worker_01
worker_02 needs-reviewer → Runtime Watchdog 检测 → 创建 reviewer_worker_02
...
worker_10 needs-reviewer → Runtime Watchdog 检测 → 创建 reviewer_worker_10

并发保证:
  1. 每个 (worker_NN, reviewer_worker_NN) 对独立
  2. NN 不同 → worktree 不同 → 产物路径不同 → 不会冲突
  3. A2A task 用 raw_key + agent_id 唯一定位
  4. Reviewer 只读自己配对的 Worker 的产物
  5. SSE 订阅按 task_id 过滤，不会收到其他 reviewer 的事件
```


## 9. agent-id.env — 工作分配的唯一真相源

### 设计原则

```
agent-table.toml          agent-id.env               freely.db (a2a_tasks)
─────────────────         ────────────               ────────────────────
定义有哪些 agent           记录"谁在哪个工位"          查询"谁空闲/谁占用"
(静态配置)                 (运行时真相)                (SQL 快速统计)
```

### agent-table.toml — 扁平化，reviewer 独立

```toml
# 旧设计 (绑定):                     # 新设计 (并列):
[[agents]]                           [[agents]]
manager_id = "manager_01"            role = "manager"
manager_slot = "..."                 manager_id = "manager_01"
reviewer_id = "reviewer_manager_01"  manager_slot = "claude-apikey-ds-pro-auto"
reviewer_slot = "..."                pool = 1
pool = 1
                                     [[agents]]
[[agents]]                           role = "worker"
worker_id = "worker_01"              worker_id = "worker_01"
worker_slot = "..."                  worker_slot = "claude-apikey-ds-pro-auto"
reviewer_id = "reviewer_worker_01"   pool = 10     # → worker_01..10
reviewer_slot = "..."
pool = 10                            [[agents]]
                                     role = "reviewer"
                                     reviewer_id = "reviewer_01"
                                     reviewer_slot = "claude-apikey-ds-pro-auto"
                                     pool = 99     # → reviewer_01..99
```

**关键变化**:
- reviewer 不再绑定在 manager/worker 下
- 命名: `reviewer_01` 不是 `reviewer_manager_01`
- pool=N 自动生成编号: worker_01..10, reviewer_01..10
- 配对不再靠 agent-table，而是靠 agent-id.env 的运行时记录

### agent-id.env — 运行时唯一真相

```
# agent-id.env — 每个工位当前由哪个 agent_working_id 工作
# ACP session/new|fork|resume 时写入，session/close 时清除
# 查询"谁在这个工位" → 读这个文件

/Users/.../freely                                    = manager_01
/Users/.../freely-worktrees/fix-raw-KEY1-xxx         = worker_03
/Users/.../freely-worktrees/test-pre-merge-KEY1-xxx  = reviewer_05
/Users/.../freely-worktrees/fix-raw-KEY2-yyy         = worker_01
/Users/.../freely-worktrees/test-pre-merge-KEY2-yyy  = reviewer_02
/Users/.../freely-worktrees/fix-raw-KEY3-zzz         = worker_07
```

**规则**:
- Manager 永远在 develop 工位 (`manager_01`)
- Worker 在 fix/raw-{key} 工位
- Reviewer 在 test-pre-merge-{key} 工位
- **一个工位可以有多个 agent** (e.g., 2 个 reviewer 审查不同面)
- ACP session 创建时写入，关闭时移除
- **以这个文件为准**，不以 agent-table 的静态配置为准

### 一个工位多个 Reviewer

```
test-pre-merge-KEY1-xxx = reviewer_05  (审查代码质量)
                         reviewer_08  (审查安全合规)
                         
agent-id.env 支持同一 worktree 多行:
/Users/.../test-pre-merge-KEY1-xxx = reviewer_05
/Users/.../test-pre-merge-KEY1-xxx = reviewer_08
```

### SQL 查询空闲 agent

```sql
-- freely.db: 哪些 agent 正在工作（占用中）
SELECT agent_id, worktree, state 
FROM a2a_tasks 
WHERE state IN ('submitted', 'working', 'input-required')
  AND agent_id LIKE 'worker_%';

-- 哪些 worker 空闲（pool=10 但未出现在占用列表）
-- Python: set(worker_01..worker_10) - set(occupied_workers)

-- 下一个可用 worker NN:
-- min(available_workers) 

-- 统计各角色占用/空闲:
SELECT 
  SUBSTR(agent_id, 1, INSTR(agent_id, '_') - 1) as role,
  COUNT(*) as occupied,
  (SELECT pool FROM agent_table WHERE agent_id = role) - COUNT(*) as free
FROM a2a_tasks 
WHERE state IN ('submitted', 'working', 'input-required')
GROUP BY role;
```

### ACP session 创建流程（修正版）

```
1. Manager 决定需要 Worker → 查 freely.db 哪个 worker_NN 空闲 → 分配 worker_03
2. Runtime ACP session/new → 写入 agent-id.env:
     fix/raw-KEY1-xxx = worker_03
3. Worker 工作完成 → needs-reviewer
4. Manager/Runtime 检测到 → 查 freely.db 哪个 reviewer_NN 空闲 → 分配 reviewer_05
5. Runtime ACP session/new → 写入 agent-id.env:
     test-pre-merge-KEY1-xxx = reviewer_05
6. Reviewer 通过 raw-key 找到 Worker 产物 → 审查
7. wt-close → session/close → 从 agent-id.env 移除对应行
```

### 配对不再靠 agent-table，靠 agent-id.env

```
旧方式: agent-table 写死配对 (reviewer_worker_01 ↔ worker_01)
新方式: agent-id.env 运行时记录

Worker 需要 Reviewer 时:
  1. 查 agent-id.env → 找到自己的 worker_NN
  2. 查 freely.db → 找到空闲的 reviewer_NN
  3. 创建 A2A task → raw_key 关联两者
  4. Reviewer 通过 raw_key 找到 Worker 的工位和产物

不需要 reviewer_NN == worker_NN。
只需要 reviewer 知道 raw_key，就能找到 Worker 的所有产物。
```


## 10. agent-id.env → agent_working_id (SQLite 表)

### 为什么用 SQLite 表代替文件

```
agent-id.env (文件)              agent_working_id (SQLite 表)
─────────────────────            ─────────────────────────────
每个 worktree 一行文本           主键 raw_key，结构化查询
多 reviewer 需重复行             一列存多个 reviewer_id
查询需 grep/awk                  SQL 直接查
无事务保护                       SQLite 事务
统计空闲 agent 需额外脚本         一条 SQL 统计占用/空闲
```

### 表结构

```sql
CREATE TABLE agent_working_id (
    raw_key         TEXT PRIMARY KEY,     -- raw-20260701T085407Z
    worktree        TEXT NOT NULL,        -- /path/to/fix/raw-KEY-slug
    branch          TEXT NOT NULL,        -- fix/raw-KEY-slug (worktree 可有多分支)
    manager_id      TEXT,                 -- manager_01 (develop 独占)
    worker_id       TEXT,                 -- worker_03
    reviewer_id     TEXT,                 -- reviewer_05,reviewer_08 (多个逗号分隔)
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### 示例数据

```sql
-- develop 工位: 只有 manager
INSERT INTO agent_working_id VALUES (
    'develop',
    '/Users/.../freely',
    'develop',
    'manager_01',
    NULL,
    NULL
);

-- fix 工位: worker_03 在工作
INSERT INTO agent_working_id VALUES (
    '20260701T085407Z',
    '/Users/.../freely-worktrees/fix-raw-20260701T085407Z-xxx',
    'fix/raw-20260701T085407Z-xxx',
    NULL,
    'worker_03',
    NULL
);

-- test 工位: 2 个 reviewer 同时审查
INSERT INTO agent_working_id VALUES (
    '20260701T085407Z',
    '/Users/.../freely-worktrees/test-pre-merge-20260701T085407Z-xxx',
    'test-pre-merge-20260701T085407Z-xxx',
    NULL,
    NULL,
    'reviewer_05,reviewer_08'
);
```

### 常用查询

```sql
-- 某个 raw_key 的工位上谁在工作？
SELECT worker_id, reviewer_id 
FROM agent_working_id 
WHERE raw_key = '20260701T085407Z';

-- 哪些 worker 正在占用中？
SELECT worker_id FROM agent_working_id WHERE worker_id IS NOT NULL;
-- → worker_03, worker_01, worker_07 (占用中)
-- → 空闲 = {worker_01..10} - {占用}

-- 下一个可用 worker NN:
-- Python: min(set(f'worker_{i:02d}' for i in range(1,11)) - occupied)

-- 某个 reviewer 在审查哪些 raw_key？
SELECT raw_key, worktree FROM agent_working_id 
WHERE reviewer_id LIKE '%reviewer_05%';

-- 统计各角色占用/空闲
SELECT 
    'worker' as role,
    COUNT(DISTINCT worker_id) as occupied,
    10 - COUNT(DISTINCT worker_id) as free
FROM agent_working_id WHERE worker_id IS NOT NULL
UNION ALL
SELECT 
    'reviewer' as role,
    COUNT(DISTINCT TRIM(v.value)) as occupied,
    99 - COUNT(DISTINCT TRIM(v.value)) as free
FROM agent_working_id, json_each('["' || REPLACE(reviewer_id, ',', '","') || '"]') v
WHERE reviewer_id IS NOT NULL;
```

### agent_working_id 与 a2a_tasks 的分工

```
agent_working_id                  a2a_tasks
─────────────────                  ─────────
"谁在哪个工位"                      "谁在做什么任务"
静态分配关系                        动态任务状态
ACP session 创建时写入              A2A task 创建/更新时写入
wt-close 时删除                    任务完成后 state=completed
查空闲 agent 用这张表              查任务进度用那张表
```


## 11. agent_working_id 表创建代码

### 建表 SQL

```sql
-- freely.db: agent_working_id table
-- Tracks which agent is working on which worktree.
-- Written at ACP session/new|fork|resume, cleared at session/close (wt-close).

CREATE TABLE IF NOT EXISTS agent_working_id (
    raw_key         TEXT PRIMARY KEY,     -- develop (for manager) or raw-YYYYMMDDTHHMMSSZ
    worktree        TEXT NOT NULL UNIQUE, -- absolute path
    branch          TEXT NOT NULL,        -- develop / fix/raw-KEY-slug / test-pre-merge-KEY-slug
    manager_id      TEXT,                 -- manager_01
    worker_id       TEXT,                 -- worker_03
    reviewer_id     TEXT,                 -- reviewer_05,reviewer_08 (comma-separated)
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_agent_working_branch ON agent_working_id(branch);
CREATE INDEX IF NOT EXISTS idx_agent_working_manager ON agent_working_id(manager_id);
CREATE INDEX IF NOT EXISTS idx_agent_working_worker ON agent_working_id(worker_id);
```

### Python 操作封装

```python
# freely-db-cli 新增命令

def agent_working_assign(raw_key, worktree, branch, role, agent_id):
    """ACP session 创建时调用。将 agent 绑定到 worktree。"""
    col = f"{role}_id"
    existing = db.get("SELECT * FROM agent_working_id WHERE raw_key = ?", [raw_key])
    if existing:
        if role == "reviewer":
            # reviewer 追加，不覆盖已有
            cur = existing.get("reviewer_id", "") or ""
            new_val = f"{cur},{agent_id}" if cur else agent_id
        else:
            new_val = agent_id
        db.execute(f"UPDATE agent_working_id SET {col} = ?, updated_at = datetime('now') WHERE raw_key = ?",
                   [new_val, raw_key])
    else:
        db.execute(f"INSERT INTO agent_working_id (raw_key, worktree, branch, {col}) VALUES (?,?,?,?)",
                   [raw_key, worktree, branch, agent_id])


def agent_working_release(raw_key, role, agent_id=None):
    """ACP session/close 时调用。释放 agent 绑定。"""
    if role == "reviewer" and agent_id:
        cur = db.get("SELECT reviewer_id FROM agent_working_id WHERE raw_key = ?", [raw_key])
        if cur and cur["reviewer_id"]:
            ids = [x.strip() for x in cur["reviewer_id"].split(",") if x.strip() != agent_id]
            db.execute("UPDATE agent_working_id SET reviewer_id = ?, updated_at = datetime('now') WHERE raw_key = ?",
                       [",".join(ids) if ids else None, raw_key])
    else:
        col = f"{role}_id"
        db.execute(f"UPDATE agent_working_id SET {col} = NULL, updated_at = datetime('now') WHERE raw_key = ?",
                   [raw_key])


def agent_working_free(role, pool_size):
    """查询空闲 agent NN 列表。"""
    col = f"{role}_id"
    prefix = f"{role}_"
    rows = db.list(f"SELECT {col} FROM agent_working_id WHERE {col} IS NOT NULL")
    occupied = set()
    for r in rows:
        val = r.get(col, "")
        if val:
            for v in val.split(","):
                occupied.add(v.strip())
    all_ids = {f"{prefix}{i:02d}" for i in range(1, pool_size + 1)}
    return sorted(all_ids - occupied)


def agent_working_next(role, pool_size):
    """返回下一个可用的 agent NN。"""
    free = agent_working_free(role, pool_size)
    return free[0] if free else None
```

## 12. 因 agent-table / agent-id 变更需修改的逻辑

### 影响面全量

```
组件                          影响                                  改动
──────────────────────────    ───────────────────────────────────  ────────
agent-table.toml              字段重构: role + {role}_id/slot      ✅ 模板已更新
                              扁平化: reviewer 独立 [[]]           agent-table-query 需重写

agent-table-query             --get-slot 参数变化                  需要适配新字段名
                              --get-reviewer 废弃                  不再需要
                              新增 --list-role --next-free         新功能

agent-id.env                  废弃，改为 agent_working_id 表       freely-db-cli 新增命令
                                                                  agent-id.env 读取逻辑全部替换

_ensure_reviewer_agent()      reviewer slot 获取方式变化           读 agent-table-query --get-slot reviewer_01
                              reviewer_id 分配逻辑                 调用 agent_working_next("reviewer", 99)

ensure_manager_once()         manager slot 获取                   保持不变 (manager_01 slot 仍读 agent-table)
                              写入 agent_working_id 表             新增

launch_worker_from_manager    worker slot 获取                    读 agent-table-query --get-slot worker_NN
                              worker_NN 分配                      调用 agent_working_next("worker", 10)
                              写入 agent_working_id 表             新增
                              agent-id.env 写入逻辑               替换为 agent_working_assign()

wt-close                      session/close 时释放 agent          调用 agent_working_release()
                              agent-id.env 清理逻辑               替换为 agent_working_id DELETE

freely-cycle                  dispatch_reviewer 时查空闲          调用 agent_working_next("reviewer", 99)
                              创建 reviewer task                  携带 agent_id, raw_key, parent_worker

a2a_server.py                 _restore_tasks()                    agent_id 前缀匹配需加 reviewer
                              agent card 生成                     从 agent-table 读 role 字段
```


## 13. Subagent 审查结论 & 最终收敛设计

### 发现的矛盾 (已解决)

| # | 矛盾 | 收敛决策 |
|---|------|---------|
| C1 | agent_working_id raw_key PK 冲突 | worktree 做主键，允许多 reviewer 行 |
| C2 | reviewer slot 继承 vs 独立 | **独立 slot**，agent-table 各配各的 |
| C3 | 静态 NN 配对 vs 运行时配对 | **运行时配对**，靠 raw_key 不靠 NN |
| C4 | _restore_tasks L442 用错变量 | 统一用局部 `agent_id` |
| C5 | Runtime 创建 task vs Manager 创建 | **Manager 创建** A2A task，Runtime 只启动 ACP |
| C6 | input-required 类型不全 | 补全双向6种 + review_stage 字段 |
| C7 | raw_key 命名不一致 | 统一 `raw-{key}` |
| C8 | pool 应该 track 还是 untracked | pool 放模板，用户可覆盖 |

### 可简化

| # | 简化 | 采纳 |
|---|------|:--:|
| S1 | 废弃 agent-id.env，直接用 SQLite | ✅ |
| S2 | reviewer_id 独立表（不用逗号分隔） | ✅ |
| S3 | 5 Phase 合并为 Foundation/A2A/Orchestration | ✅ |
| S4 | 3 个 card 文件合并为 1 个 roles.toml | ✅ |
| S5 | 移除 Manager 初始 A2A task | ✅ |
| S6 | agent_working 简化 schema | ✅ |

### 最终 agent_working 表

```sql
CREATE TABLE agent_working (
    worktree    TEXT NOT NULL PRIMARY KEY,
    agent_id    TEXT NOT NULL,
    role        TEXT NOT NULL CHECK(role IN ('manager','worker','reviewer')),
    raw_key     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

## 14. 最终 TODO List (按依赖排序)

### Phase 0: Foundation — Bug Fix + Schema

- [ ] P0.1 修 a2a_server.py _restore_tasks 三处 and/or 优先级 bug (L403, L442, L663)
- [ ] P0.2 建 agent_working 表 (migration SQL)
- [ ] P0.3 实现 agent_working.py CRUD (assign/release/list_by_role/next_free)

### Phase 1: Agent-Table v2

- [ ] P1.1 确认 .freely/agent-table.toml v2 格式 (已完成 ✅)
- [ ] P1.2 重写 agent-table-query (废弃 --get-reviewer, 新增 --next-free)
- [ ] P1.3 全局替换 agent-id.env → agent_working 表

### Phase 2: ACP Session

- [ ] P2.1 _ensure_reviewer_agent() 接受 reviewer_id + parent_worktree 参数
- [ ] P2.2 ensure_manager_once() 写 agent_working 表
- [ ] P2.3 launch_worker_from_manager() 用 agent_working.next_free + assign
- [ ] P2.4 wt-close 释放 agent_working

### Phase 3: A2A Multi-Card + Task

- [ ] P3.1 agent-card 端点支持 ?role= 参数
- [ ] P3.2 Manager 通过 POST /tasks 委派 Worker/Reviewer
- [ ] P3.3 PATCH /tasks/{id} SSE 推送 + 订阅过滤
- [ ] P3.4 task 增加 review_stage 字段

### Phase 4: Watchdog SSE

- [ ] P4.1 Runtime Watchdog 订阅 SSE + 重连
- [ ] P4.2 SSE 事件处理: needs-review → 创建 Reviewer session
- [ ] P4.3 轮询降级为 fallback
- [ ] P4.4 任务僵死检测

### Phase 5: Card + input-required 补全

- [ ] P5.1 创建 docs/system/workspace/agents/roles.toml
- [ ] P5.2 input-required 双向路由补全
- [ ] P5.3 wt-close 生命周期集成
- [ ] P5.4 freely-cycle dispatch_reviewer 实际执行

