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

