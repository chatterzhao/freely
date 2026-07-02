# Review 09: Routa vs Freely 架构对比

- date: 2026-07-02
- routa: https://github.com/phodal/routa (MIT, TypeScript+Rust, ~1.7k stars)
- freely: chatterzhao/freely (Shell+Python, private)

---

## 1. 核心哲学

| 维度 | Routa | Freely |
|------|-------|--------|
| **隐喻** | Kanban（看板） | IBM Framework（I→B→M 四节点链路） |
| **设计原则** | "下游不信任上游" — 每个 Specialist 先验证上游产物 | "逐环消化" — 每个 Loop 先 Review 再推进 |
| **产品形态** | Web App (Next.js) + Desktop (Tauri) | 纯 CLI + Daemon（Shell 脚本驱动） |
| **用户入口** | Kanban 看板 UI + Chat 面板 | `freely feedback` → `freely wt-create` → 自动化 |
| **目标** | 人+AI 协作的软件交付平台 | AI 自治持续交付循环 |

**相同点**：两者都是"编排多个 AI CLI 工具（Claude Code、Codex CLI 等）完成软件交付"。

**不同点**：Routa 是**产品**（有 UI，人参与看板拖动），Freely 是**自治系统**（daemon 自动巡逻、委派、收口）。

---

## 2. 技术栈对比

### Routa（TypeScript + Rust 双运行时）

```
┌─ Web 运行时 (Next.js) ──────────────────────────┐
│  src/core/routa-system.ts  ← 中央装配点          │
│  src/core/acp/              ← ACP 适配层          │
│  src/core/events/event-bus.ts ← 进程内事件总线    │
│  + 12+ Store 接口 (AgentStore, TaskStore, ...)    │
└──────────────────────────────────────────────────┘
┌─ Desktop 运行时 (Tauri + Axum) ──────────────────┐
│  crates/routa-core/src/acp/   ← Rust ACP 子系统   │
│  crates/routa-core/src/orchestration/ ← 编排引擎  │
│  crates/routa-core/src/events/ ← Rust EventBus    │
│  + Postgres/SQLite/InMemory 三套 Store 实现       │
└──────────────────────────────────────────────────┘
```

### Freely（Shell + Python 单运行时）

```
┌─ CLI + Daemon 运行时 (Shell 驱动) ───────────────┐
│  docs/system/workspace/scripts/runtime/freely     │
│    (~25k 行 Shell) ← 全部编排逻辑                  │
│  docs/system/workspace/scripts/runtime/            │
│    acp-bridge.py          ← ACP 桥接（852行）      │
│    freely_db_manager.py   ← SQLite 守护进程        │
│    a2a/a2a_server.py      ← A2A 协议服务器          │
│    watchdog_sse.py        ← SSE 看门狗（360行）     │
│    agent_working.py       ← Agent 工作表 CRUD      │
│  + SQLite 单数据库（freely.db）                    │
└──────────────────────────────────────────────────┘
```

**关键差异**：
- Routa 有 Rust 侧——ACP 进程 spawn、Sandbox、编排逻辑都用 Rust 实现，性能高
- Freely 全是 Shell/Python——编排逻辑用 Shell 函数、RPC 走 Unix Socket、ACP 用 Python
- Routa 的 `routa-system.ts` 是**服务容器模式**（DI），Freely 是**函数调用模式**（bash 函数）

---

## 3. Agent 角色模型

### Routa：5+ Specialist 角色

```
Backlog → Todo → Dev → Review → Done
(Refiner) (Orchestrator) (Crafter) (Guard) (Reporter)
```

| Specialist | 泳道 | 输入 | 产出 |
|-----------|------|------|------|
| Backlog Refiner | Backlog | 模糊需求 | Canonical YAML Story（AC+约束） |
| Todo Orchestrator | Todo | Story | Execution Brief（执行计划） |
| Dev Crafter | Dev | Execution Brief | Dev Evidence（代码+测试+commit） |
| Review Guard | Review | Dev Evidence | Review Findings（逐条AC判定） |
| Done Reporter | Done | Review Findings | Completion Summary |

上方还有 **ROUTA Coordinator** —— 规划、拆解、委派，不直接编码。

### Freely：3 角色 + 6 向 input-required

```
Manager (develop 工位)     ←→  Worker (fix/raw-{key} 工位)
    ↕                           ↕
Reviewer (test-pre-merge-{key} 工位)
```

| 角色 | 工位 | 职责 |
|------|------|------|
| Manager | develop | 巡逻、委派、收口 |
| Worker | fix/raw-{key} | B1/B2/RED/dev/test 全流程 |
| Reviewer | test-pre-merge-{key} | 每步审查、门禁检查 |

**6 向路由**（InputRequiredReason Enum）：
1. Worker → Reviewer（needs-review:b1/b2/dev/red/test/gate）
2. Worker → Manager（needs-manager-decision）
3. Reviewer → Worker（needs-worker-retry）
4. Reviewer → Manager（needs-manager-scope）
5. Manager → Reviewer（needs-review:gate）
6. Manager → Worker（needs-worker-task）
7. 兜底 → Manager_01（unknown）

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| 角色数 | 5+ Specialist + Coordinator | 3 角色（Manager/Worker/Reviewer） |
| 专用性 | 每个泳道专属 Specialist | Worker 承担 B1~test 全流程 |
| 分工方式 | 按**泳道**（Backlog→Dev→Review） | 按**阶段**（B1→B2→RED→dev→test） |
| 并行 | Crafter 可并行 fan-out | Worker 串行执行（单 raw_key 单 Worker） |
| 委派者 | Coordinator 自动拆解委派 | Manager patrol 发现后委派 |

**Freely 的 Worker 承担的职责，在 Routa 中被拆分成了多个 Specialist**（Refiner → Orchestrator → Crafter → Guard → Reporter）。Freely 的优势是简单（3 角色），劣势是 Worker 过重。

---

## 4. 任务/工作流模型

### Routa：Kanban Lane 状态机

```
Backlog ──→ Todo ──→ Dev ──→ Review ──→ Done
  ↑          ↑        ↑        ↑
  └── 退回 ──┴── 退回 ─┴── 退回 ─┘
              (任何阶段可进 Blocked)
```

**泳道合同（Lane Contract）**：每个泳道有明确的**输入要求**和**产出要求**，下游先验证上游。
- Backlog → canonical YAML Story（INVEST 检查）
- Todo → Execution Brief（重校验上游，补齐执行计划）
- Dev → Dev Evidence（逐条 AC 验证记录 + commit）
- Review → Verdict（独立逐条验证，不信任 Dev 的自查）

**卡片是信息载体**：同一张卡片在流转中不断被补全，Backlog 写 Story、Todo 写 Plan、Dev 写 Evidence、Review 写 Findings。

### Freely：三 Loop + 四节点链路

```
Loop 1: Doc Loop (发现/设计)
  Manager patrol → Worker B1 → Reviewer 审查 → Worker B2 → Reviewer 审查

Loop 2: Dev Loop (执行/验证)
  RED → Reviewer → dev → Reviewer → test-GREEN → Reviewer

Loop 3: Auto Loop (收口/治理)
  pr-create → pr-review → pr-merge → wt-close
  Runtime: restart, crash recovery, cleanup
```

**四节点链路**（IBM Framework）：
```
raw issue → candidate (C-{key}-A) → milestone (M-{key}-A) → I-* issue (I-{key}-A)
```

**产物流**：
- raw issue → brainstorms.md + candidates.md（B1）
- candidate promoted → prd.md + pre-tests.md + tasks.md（B2）
- RED → actual_RED_output evidence
- dev → code-review + Implementation Decision Note
- test → GREEN evidence（test-pre-merge 工位）

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| 工作流模型 | Kanban 泳道（5列） | 三 Loop + 四节点（raw→candidate→milestone→I-*） |
| 状态机 | 简单（Todo↔Dev↔Review→Done） | 复杂（B1→B2→RED→dev→test→PR→merge→close） |
| 信息载体 | 卡片（持续补全的 Note） | issue.md + brainstorms.md + pre-tests.md + ... |
| 交互方式 | 人拖看板 → AI 执行 → 人验证 → 继续 | AI 自驱动（daemon 巡逻 → 自动委派 → 自动收口） |
| Review 位置 | Review 是独立泳道（Dev 后） | Review 在每个阶段后（B1/B2/RED/dev/test/PR） |
| 并发 | Task 级别 fan-out | raw_key 级别串行 |
| 人参与 | UI 拖拽 + Chat | `freely feedback` 命令 |

**核心差异**：Routa 的看板是**人驱动的编排层**（人决定什么时候卡片进入下一列），Freely 的 Loop 是 **AI 自驱动的构建层**（daemon 自动巡逻、自动判断下一跳）。

---

## 5. ACP（Agent Client Protocol）用法对比

### Routa：ACP 是核心执行协议

```
RoutaOrchestrator.delegateTaskWithSpawn(params) →
  AcpManager.create_session() →
    启动真实 OS 进程（stream-json stdin/stdout 通信）→
      写入 AcpSessionStore（Postgres/SQLite/InMemory）
```

- **`DelegateWithSpawnParams`** 包含：task_id, caller_agent_id, caller_session_id, workspace_id, specialist（CRAFTER/GATE/DEVELOPER）, provider, cwd, wait_mode
- **wait_mode**: `"immediate"`（立即返回）或 `"after_all"`（等待完成）
- **session ID 三层嵌套**: `routaAgentId` → `sessionId` → `sdkSessionId`
- **冷启动恢复**: Serverless 环境从 Postgres 查 `acp_sessions` 表恢复 adapter
- **子进程隔离**: 独立 PID + 独立 cwd（worktree）+ 独立 MCP URL + 委托深度限制（max 2 层）

### Freely：ACP 是 Runtime 创建的 session

```
_acp_session_new(project, role, agent_id, raw_key) →
  Unix Socket JSON-RPC → acp-bridge.py →
    claude-agent-acp session/new →
      写入 agent_working 表（agent_id:session_id）
```

- **ACP 桥接**: `acp-bridge.py`（852 行）封装 `claude-agent-acp` SDK
- **session ID 格式**: `{role}_{timestamp}_{agent_id}`
- **session/fork**: 同 tool 复用连接
- **session/resume**: daemon 重启时从 `agent_working` 表恢复
- **session/close**: wt-close 时释放
- **子进程隔离**: 独立 PID + 独立 worktree（git worktree add）

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| ACP 实现 | Rust `AcpManager` + TypeScript 适配层 | Shell 函数 `_acp_session_new` + Python 桥接 |
| Session 存储 | 专用 `acp_sessions` 表（Postgres/SQLite） | `agent_working` 表（agent_id:session_id 格式） |
| 子进程管理 | Rust 进程管理（prompt/cancel/kill/subscribe） | Shell `nohup` + PID file |
| 冷启动恢复 | Postgres 查 `acp_sessions` → 重建 adapter | `_restore_tasks` + `agent_working.get_all` |
| 委托方式 | `delegateTaskWithSpawn(params)` 结构化参数 | `freely-cycle` 轮询 + `agent_assign` |
| Provider 支持 | 多 Provider 适配（Claude Code/Codex/Gemini/OpenCode/Kimi/Augment） | 多 Provider 适配（Claude/Codex/OpenCode via acp-bridge） |

**Routa 的 ACP 层更成熟**：Rust 实现、结构化参数、冷启动恢复、session store 独立表。Freely 的 ACP 层更轻量：Shell+Python、agent_working 表复用、Unix Socket RPC。

---

## 6. 数据库设计

### Routa：多 Store + 多驱动

```
Store 接口层（TS + Rust）:
  AgentStore, TaskStore, NoteStore, ConversationStore,
  AcpSessionStore, BackgroundTaskStore, WorktreeStore,
  CodebaseStore, WorkspaceStore, KanbanStore, ScheduleStore,
  WorkflowRunStore, ArtifactStore (12+ 个独立 Store)

驱动层:
  ├─ PostgreSQL（Neon serverless / 标准 postgres-js）
  ├─ SQLite（better-sqlite3, WAL 模式）
  └─ InMemory（Map, 不持久化）

Migration: Drizzle Kit (PG) + 启动时 CREATE TABLE IF NOT EXISTS (SQLite)
```

### Freely：单数据库 + RPC Handler

```
freely.db (SQLite, 单文件):
  chats, sessions, discussions, tool_switch_events,
  task_mode_gate, tool_failure_log, a2a_tasks,
  agent_working (8 张表)

RPC 层: freely_db_manager.py
  @_h("xxx") 装饰器注册 RPC handler → Unix Socket JSON-RPC
  所有 CRUD 通过 socket 调用，不直接 sqlite3.connect()
```

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| Store 数量 | 12+ 独立 Store 接口 | 8 张表，按需在 `agent_working.upsert` 等 RPC 操作 |
| 驱动 | PostgreSQL / SQLite / InMemory | 仅 SQLite |
| DDL 管理 | Drizzle Kit migration + 启动时 ALTER TABLE | 启动时 `CREATE TABLE IF NOT EXISTS` + `ALTER TABLE` 迁移 |
| ORM | Drizzle ORM | 原生 `sqlite3` cursor |
| 访问层 | Store 接口（TS DI 注入） | Unix Socket RPC（`@_h` 装饰器） |

**Routa 的数据库层更工程化**：多驱动适配、Drizzle ORM、Migration 管理、Store 接口抽象。Freely 更直接：SQLite 单文件 + RPC handler + 原生 SQL。

**一个有趣的共同点**：两者都用 `agent_working`/`acp_sessions` 表来跟踪 agent 进程和 session 绑定。Routa 用独立的 `acp_sessions` 表（session 是核心实体），Freely 把 session_id 嵌入 `agent_working` 的列值中（`agent_id:session_id` 格式）。

---

## 7. 进程/运行时模型

### Routa：Tauri 桌面 App + Next.js Web

```
[Routa Desktop]                [Routa Web]
Tauri Shell                    Next.js App Router
  └─ Axum Backend              └─ API Routes
       └─ RoutaOrchestrator         └─ RoutaSystem
            └─ AcpManager                └─ AcpManager
                 └─ spawn 子进程               └─ spawn 子进程
```

- **进程管理**：Rust 的 `AcpManager` 管理子进程生命周期（spawn/prompt/cancel/kill）
- **后台任务**：`BackgroundTaskStore` 管理定时/轮询/webhook 触发的任务
- **Sandbox**：Docker 沙箱支持（`crates/routa-core/src/sandbox/`）
- **SSE**：实时增量更新到 UI

### Freely：Shell Daemon + Python Scripts

```
[Freely Daemon]
Shell 脚本驱动 (docs/system/workspace/scripts/runtime/freely)
  ├─ Supervisor (freely supervisor)
  ├─ AI 进程 (freely ai)
  ├─ ACP Bridge (freely acp-bridge)
  ├─ Manager Watchdog (freely ensure-manager)
  ├─ SSE Watchdog (freely ensure-sse-watchdog)
  ├─ Python SSE Watchdog (watchdog_sse.py)
  ├─ A2A Server (a2a_server.py)
  └─ Dispatcher (interruption)
```

- **进程管理**：Shell 的 `nohup` + PID file 模式
- **看门狗**：Shell watchdog（轮询）+ Python watchdog（SSE 事件驱动）
- **A2A Server**：Starlette + Uvicorn（Unix socket）
- **DB Manager**：Python daemon（Unix socket RPC）
- **SSE**：A2A Server → SSE subscriber → watchdog 处理

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| 进程管理 | Rust `AcpManager`（强类型、结构化） | Shell `nohup` + PID file（弱类型、字符串） |
| 运行时启动 | Tauri App 或 Next.js 启动 | `freely start` 命令 |
| 子进程通信 | stream-json stdin/stdout | ACP bridge Unix socket |
| 后台任务 | BackgroundTaskStore + EventBus | Manager watchdog 轮询 + cron |
| Sandbox | Docker | Git worktree 隔离 |
| 崩溃恢复 | Postgres 恢复 session + 重建 adapter | agent_working 表恢复 + _restore_tasks |

**Routa 的进程模型更现代**：Rust 管理进程生命周期、类型安全、Sandbox 支持。Freely 的进程模型更 Unix 原生：Shell 的 PID file + nohup + signal handling，契合"Shell 驱动一切"的哲学。

---

## 8. 事件/通信模型

### Routa：EventBus + MCP + A2A + SSE + AG-UI

```
RoutaOrchestrator
  └─ delegateTaskWithSpawn()
       └─ AcpManager.create_session()
            └─ 子进程通过 MCP 工具连接回 Routa
                 ├─ read_note / update_note
                 ├─ delegate_task_to_agent
                 └─ report_to_parent
                      └─ EventBus.emit(REPORT_SUBMITTED)
                           └─ Orchestrator 唤醒父 Agent
```

**EventBus 三种高级模式**（TypeScript）：
- `oneShot` — 一次性订阅
- `priority` — 优先级排序
- `waitGroup` — 等待所有 Agent 完成后回调

### Freely：A2A SSE + ACP Bridge Unix Socket

```
Worker (ACP session) → A2A task PATCH (state: input-required)
  → A2A Server._notify_sse()
    → SSE global stream → watchdog_sse.py
      → _handle_sse_event() → InputRequiredReason 路由
        → _acp_session_new/resume → Reviewer ACP session
```

**通信协议栈**：
- **A2A**：agent ↔ agent（task 生命周期、state machine、SSE 推送）
- **ACP**：agent ↔ AI CLI tool（session 管理、prompt）
- **Unix Socket RPC**：freely 函数 ↔ freely_db_manager（DB 操作）
- **SSE**：A2A Server → watchdog → 事件驱动调度

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| 核心通信 | MCP（工具调用）+ EventBus（进程内事件） | A2A（agent 间）+ ACP（agent-tool）|
| 父唤醒机制 | `report_to_parent` MCP tool → EventBus → Orchestrator | A2A SSE → watchdog → ACP session/resume |
| 事件总线 | Typed EventBus（TS + Rust 双实现） | 无独立事件总线，SSE 流即事件通道 |
| 协议数量 | REST + MCP + ACP + A2A + AG-UI + SSE（6 协议） | ACP + A2A + Unix Socket RPC + SSE（4 协议） |

**Routa 的 MCP 工具回连模式很巧妙**：子 Agent 通过 MCP 工具（`read_note`、`report_to_parent`、`delegate_task_to_agent`）与父系统交互。Freely 的 A2A SSE 模式也很巧妙：Worker 只需更新 A2A task 状态（`state: input-required`），watchdog 自动路由到 Reviewer。

---

## 9. Review/Gate 模型

### Routa：三层 Gate 架构

```
Review 阶段 ──→ Harness Monitor（发生了什么）
                  ├─ traces、变更文件、命令输出、git 状态
              ──→ Entrix Fitness（硬性门禁）
                  ├─ 文件预算、策略检查、测试通过
              ──→ Gate Specialist（AC 判定）
                  ├─ 逐条 AC → APPROVED / REJECTED / 升级人工
```

**核心原则**："下游不信任上游"。Review Guard **必须独立验证**，不能用 Dev Crafter 的自查报告替代。

### Freely：IBM 四级审查 + Gate

```
B1 → Reviewer 审查（brainstorms.md + candidates.md 质量）
B2 → Reviewer 审查（PRD/pre-tests 是否覆盖改动面）
RED → Reviewer 审查（actual_RED_output 不是 placeholder）
dev → Reviewer 审查（代码是否按 TDD 实现）
test → Reviewer 审查（GREEN 证据是否真实）
PR → Gate 自动检查（epics-map, IBM lifecycle, commit 完整性）
merge → Gate 自动检查（merge receipt, governance, pretests-retirement）
```

**核心原则**："逐级消化"。每个阶段都必须 Review 通过才能进入下一阶段。

**关键差异**：

| 维度 | Routa | Freely |
|------|-------|--------|
| Review 层数 | 3 层（Harness → Fitness → Gate） | 7 层（B1/B2/RED/dev/test/PR/merge） |
| Review 角色 | 独立 Gate Specialist | Reviewer + 自动 Gate |
| 判定粒度 | 逐条 AC 验证 | 逐阶段产物审查 |
| 不通过处理 | 退回上一泳道 | Reviewer 写 guidance → Worker 重做 |
| 自动/人工 | Gate 人工判定 | PR/merge Gate 自动，其余 Reviewer AI |

**Routa 的 Review 更结构化**：三层 Gate 分层明确、逐条 AC 判定、Harness 提供 traces。Freely 的 Review 更密集：每个阶段都审查，但缺少 Routa 那种"三层 Gate"的分层设计。

---

## 10. 具体场景对比：一个 Bug Fix 的完整流程

### Routa 流程

```
1. 人在 Kanban Backlog 创建卡片（写 YAML Story + AC）
2. Backlog Refiner 完善 Story（INVEST 检查）
3. 人把卡片拖到 Todo
4. Todo Orchestrator 重校验 → 补 Execution Plan
5. 人把卡片拖到 Dev
6. Dev Crafter spawn（ACP session/new, worktree 隔离）
   → 写代码 → 自测 → 提交 → report_to_parent
7. 人把卡片拖到 Review
8. Review Guard spawn → 逐条 AC 验证 → APPROVED / REJECTED
9. 人把卡片拖到 Done → Done Reporter 写 Completion Summary
```

**人参与点**：拖卡（4次）—— Backlog→Todo→Dev→Review→Done

### Freely 流程

```
1. Manager patrol（daemon 自动扫描新 issue）
2. Manager wt-create（自动创建 worktree + branch）
3. Worker B1 → 产出 brainstorms.md + candidates.md
4. Worker PATCH a2a_task（state: input-required, reason: needs-review:b1）
5. A2A SSE → watchdog → Reviewer ACP session/new → 审查 → pass/fail
6. pass → Worker B2 → Reviewer 审查 → pass
7. pass → RED → Reviewer 可选审查 → pass → dev → Reviewer 审查 → pass
8. pass → test-GREEN → Reviewer 审查 → pass
9. pr-create → pr-review → pr-merge → wt-close（自动）
```

**人参与点**：1次（`freely feedback` 触发初始 issue）—— 其余全自动

**核心差异**：Routa 是**人拖看板驱动 AI**，Freely 是 **AI 自驱动完成全流程**。

---

## 11. 优劣势总结

### Routa 的优势

1. **结构化程度高**：YAML Story + AC + Execution Plan + Evidence → 可追溯、可审计
2. **类型安全**：Rust + TypeScript，编译期检查
3. **多驱动数据库**：Postgres + SQLite + InMemory，适合 Serverless
4. **冷启动恢复**：从 Postgres 恢复 ACP session，适合云部署
5. **进程管理成熟**：Rust `AcpManager` 的结构化进程管理
6. **有 UI**：Web + Desktop，人可以直接看 Kanban、拖卡片
7. **MCP 工具回连**：子 Agent 通过 MCP 工具与父系统交互，模式优雅
8. **三层 Gate**：Harness（trace）+ Fitness（硬门禁）+ Gate（AC 判定），分层清晰

### Routa 的劣势

1. **技术栈重**：Next.js + Tauri + Rust + TypeScript，4 个运行时
2. **人的参与度高**：需要人拖看板、人写 Story、人判断放行
3. **Kanban 隐喻限制**：适合"一个卡片 = 一个任务"的粒度，不适合长周期多阶段交付
4. **无自治循环**：没有"daemon 自动巡逻 → 自动委派 → 自动收口"的闭环

### Freely 的优势

1. **自治程度高**：daemon 自动巡逻 → 自动委派 → 自动审查 → 自动收口
2. **技术栈轻**：Shell + Python，单一 SQLite DB，部署简单
3. **IBM Framework 成熟**：raw → candidate → milestone → I-* issue，四节点链路严格
4. **三 Loop 模型**：L1 Doc → L2 Dev → L3 Auto，覆盖完整交付生命周期
5. **Git Worktree 隔离**：每个 raw_key 独立 worktree，test-pre-merge 测试工位
6. **6 向 input-required 路由**：覆盖所有 agent 间通信场景
7. **人参与少**：`freely feedback` 一次触发，后续全自动

### Freely 的劣势

1. **Shell 可维护性**：25k 行 Shell 脚本，类型不安全
2. **无 UI**：纯 CLI，远程看不到状态
3. **数据库简单**：单 SQLite，不适合分布式
4. **进程管理原始**：PID file + nohup，缺少结构化进程管理
5. **无 Sandbox**：只靠 git worktree 隔离
6. **无冷启动恢复**：依赖本地 agent_working 表
7. **事件系统弱**：SSE 即事件通道，缺少 EventBus 抽象
8. **Worker 过重**：一个 Worker 承担 B1→B2→RED→dev→test 全流程

---

## 12. 可借鉴的设计

### 从 Routa 可以学什么

1. **卡片作为信息载体**：Freely 的 issue.md 可以增加类似 Routa 的结构化 YAML（AC + constraints + evidence），让 Reviewer 的审查更有依据

2. **三层 Gate 分层**：Freely 的 Reviewer 可以借鉴 Harness（trace）→ Fitness（门禁）→ Gate（判定）三层结构，而不是让 Reviewer 一次性审查所有方面

3. **MCP 工具回连**：Freely 的 Worker/Reviewer 通过 A2A SSE 通信，但可以增加 MCP 工具让 Agent 回连到 Runtime 查询状态（如 `read_note` → 读 issue.md frontmatter）

4. **EventBus + waitGroup**：Freely 的看门狗可以借鉴 EventBus 模式，而不是纯 SSE 流处理。`waitGroup` 模式特别适合"等待所有 Worker 完成"的场景

5. **Structured DelegateWithSpawnParams**：Freely 的 `agent_assign` 可以用类似的结构化参数（task_id, caller_agent_id, specialist, provider, wait_mode），而不是隐式依赖 agent_working 表

6. **AcpSessionStore 独立表**：Freely 的 `agent_working` 表混合了 worktree 绑定和 session 管理。借鉴 Routa 独立 `acp_sessions` 表可以让 session 生命周期更清晰

7. **Cold Start Recovery**：Freely 的 `_restore_tasks` 已经实现了 daemon 重启恢复，但可以借鉴 Routa 的 Postgres 冷启动模式（当 agent_working 表丢失时从其他来源恢复）

### Routa 可以从 Freely 学什么

1. **自治闭环**：Routa 的 Kanban 需要人拖动，Freely 的 daemon 自动巡逻是更彻底的自治

2. **三 Loop 模型**：L1 Doc → L2 Dev → L3 Auto 的分层比单一看板更贴合软件交付的节奏

3. **Git Worktree 隔离**：Freely 的 dev + test-pre-merge 双工位模式比 Routa 的单 worktree 更安全

4. **input-required 路由枚举**：InputRequiredReason Enum 的全仓一致性约束比自由字符串更可靠

5. **agent_working 表**：把 agent 绑定和 session 管理放在一张表中（raw_key 为主键）比分散在多个 Store 中更简单

---

## 结论

**Routa** 是一个优秀的**人+AI 协作的看板平台**，设计理念是"让看板成为任务协议"——结构化卡片、泳道合同、三层 Gate。它适合团队协作、需要人参与的软件交付场景。

**Freely** 是一个激进的 **AI 自治交付系统**，设计理念是"让 AI 自己跑完整个交付流程"——daemon 巡逻、三 Loop 推进、逐环审查。它适合单个 AI 持续交付的场景。

**两者的共同方向**：通过结构化协议（ACP/A2A/MCP）编排多个 AI CLI 工具，用协议化的工作流（Kanban/IBM Framework）替代自由文本交互。

**Freely 下一步可以借鉴的优先级**：
- P0: 结构化 AC（让 Reviewer 有明确的验收标准可对照）
- P1: 三层 Gate 分层（Harness → Fitness → Gate）
- P2: EventBus 抽象（替代纯 SSE 事件处理）
- P3: AcpSessionStore 独立表（解耦 worktree 绑定和 session 管理）
