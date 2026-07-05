---
b1_id: B1-20260701T085407Z
phase_state: completed
source_raw: raw-20260701T085407Z07Z
source_url: https://github.com/chatterzhao/freely/issues/3697
produced_candidate: C-20260701T085407Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A reviewer agent — 最终收敛架构 + TODO

## 1. 最终收敛架构

### 三角色 + Worktree 绑定

| 角色 | 工位 | Agent ID | 职责 |
|------|------|---------|------|
| Manager | develop | manager_01 | 巡逻、委派、收口 |
| Worker | fix/raw-{key} | worker_01..10 | B1/B2/RED/dev/test |
| Reviewer | test-pre-merge-{key} | reviewer_01..99 | 每步审查、门禁检查 |

### ACP vs A2A

```
ACP: agent ↔ AI CLI tool (垂直，装大脑)
A2A: agent ↔ agent        (水平，协作)

ACP 管: session/new|fork|resume|close, slot, conversation_id
A2A 管: task 生命周期, agent card, SSE 推送, state machine
两者正交。同一 ACP process 多 session。同一 A2A task 跨 daemon 重启。
```

### agent-table.toml v2 (扁平)

```toml
[[agents]]                          [[agents]]
role = "manager"                    role = "worker"
manager_id = "manager_01"           worker_id = "worker_01"
manager_slot = "..."                worker_slot = "..."
pool = 1                            pool = 10

[[agents]]
role = "reviewer"
reviewer_id = "reviewer_01"
reviewer_slot = "..."
pool = 99
```

### agent_working 表 (SQLite)

```sql
CREATE TABLE agent_working (
    raw_key         TEXT PRIMARY KEY,
    worktree        TEXT NOT NULL,
    branch          TEXT NOT NULL,
    test_worktree   TEXT,
    test_branch     TEXT,
    manager_id      TEXT,       -- manager_01:ses_abc
    worker_id       TEXT,       -- worker_03:ses_def
    reviewer_id     TEXT,       -- reviewer_05:ses_ghi,reviewer_08:ses_jkl
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

值格式: `agent_id:session_id`。无 session 时仅有 agent_id。
reviewer 逗号隔开多个 `agent_id:session_id` 对。agent-id.env 完全废弃。

### Runtime Watchdog = Bootstrapper

```
Runtime 介入 (ACP session)     Runtime 不介入 (A2A SSE 直连)
─────────────────────────     ─────────────────────────────
检测 needs-review              Worker↔Reviewer 互推状态
Reviewer 不存在 → 创建 ACP     Reviewer→Worker verdict 推送
Agent crash → 重新启动         正常 state 变更
Daemon 重启 → resume           working/completed 更新
```

### 配对：靠 raw_key，不靠 NN

worker_03 和 reviewer_05 无需 NN 匹配。通过 raw_key 关联：
同一 raw_key 的 dev worktree 和 test worktree，A2A task 携带 raw_key + parent_agent。

### input-required 路由 (6 向 + 兜底)

| # | 方向 | reason | 处理者 | ACP |
|---|------|--------|--------|-----|
| 1 | Worker→Reviewer | needs-review:b1/b2/dev | Reviewer | session/fork 或 new |
| 2 | Worker→Manager | needs-manager-decision | Manager | session/resume |
| 3 | Reviewer→Worker | needs-worker-retry | Worker | session/resume |
| 4 | Reviewer→Manager | needs-manager-scope | Manager | session/resume |
| 5 | Manager→Reviewer | needs-review:gate | Reviewer | session/new |
| 6 | Manager→Worker | needs-worker-task | Worker | session/resume/fork |
| **兜底** | **任何人** | **未识别 / 空 / 未知** | **manager_01** | **session/resume** |

兜底规则: reason 不匹配上述 6 种、为空、或解析失败时，一律路由到 manager_01。

### input-required 事件完整参数

```json
{
  "task_id":       "uuid",                    // A2A task ID
  "from_agent":    "worker_03",               // 谁发出的
  "from_role":     "worker",                  // manager|worker|reviewer
  "from_worktree": "/path/to/fix/raw-KEY",   // 发出方工位
  "from_branch":   "fix/raw-KEY-slug",       // 发出方分支
  "needs_agent":   "reviewer_05",             // 需要谁来处理 (路由决定)
  "needs_role":    "reviewer",                // manager|worker|reviewer
  "raw_key":       "20260701T085407Z",        // 哪个 issue
  "state":         "input-required",          // 当前状态
  "reason":        "needs-review:b1",         // 为什么需要 (路由 key)
  "review_stage":  "b1",                      // b1|b2|dev|red|test|gate (可选)
  "skill":         "freely-tdd-review",       // 需要执行的 skill (可选)
  "message":       "B1 完成，请审查",          // 人类可读描述
  "parent_agent":  "manager_01",              // 谁委派的原始任务 (可选)
  "session_id":    "ses_abc123",              // 发出方 ACP session (可选)
  "timestamp":     "2026-07-01T08:00:00Z"    // 事件时间
}
```

`reason` = 为什么 (问题类型), `needs_agent` = 找谁 (路由结果)。

### reason vs message — A2A 协议对齐

```
A2A TaskStatusUpdateEvent (完整协议路径):
  ├── status.message   → message  (A2A 标准字段, Message + Part(text))
  └── metadata         → reason + from_agent + needs_agent + raw_key + ...
                          (Freely 自定义, metadata dict)

内部 SSE 推送 (简化路径, _notify_sse 直出):
  {"task_id": "...", "state": "input-required", "reason": "needs-review:b1",
   "from_agent": "worker_03", "needs_role": "reviewer", "raw_key": "...", ...}
  所有字段平铺在顶层，不套 statusUpdate。
```

| 字段 | 存在 A2A 哪里 | 消费者 | 格式 | 一致性保证 |
|------|-------------|--------|------|-----------|
| reason | metadata | Runtime Watchdog 路由 | 枚举值, 不可随意写 | InputRequiredReason Enum |
| message | status.message | 接收方 agent (AI) | 自然语言 | 自动生成模板 |

### reason 枚举 (Freely 代码定义，全仓一致)

```python
# docs/system/workspace/agents/input_required_reason.py
from enum import Enum

class InputRequiredReason(Enum):
    NEEDS_REVIEW_B1 = "needs-review:b1"
    NEEDS_REVIEW_B2 = "needs-review:b2"
    NEEDS_REVIEW_DEV = "needs-review:dev"
    NEEDS_REVIEW_RED = "needs-review:red"
    NEEDS_REVIEW_TEST = "needs-review:test"
    NEEDS_REVIEW_GATE = "needs-review:gate"
    NEEDS_MANAGER_DECISION = "needs-manager-decision"
    NEEDS_WORKER_RETRY = "needs-worker-retry"
    NEEDS_MANAGER_SCOPE = "needs-manager-scope"
    NEEDS_WORKER_TASK = "needs-worker-task"
    NEEDS_HUMAN_INPUT = "needs-human-input"
    UNKNOWN = "unknown"  # 兜底 → manager_01
```

所有 agent 必须使用此 Enum 写入 reason，禁止手写字符串。
新增 reason 时先改 Enum 再改路由表，编译器/IDE 保证不遗漏。

### message 自动生成

agent 设 input-required 时不手写 message。Runtime 根据参数自动生成：

```
模板: "{from_agent} 在 raw_key={raw_key} 完成 {review_stage}，需要 {reason}。
       产物路径: docs/B2-docs/{epic}/{story}/raw-{raw_key}/..."

示例: "worker_03 在 raw-20260701T085407Z07Z 完成 B1，需要 needs-review:b1。
       产物路径: docs/B2-docs/a2a/phase1/raw-20260701T085407Z07Z/..."
```

message 保证接收方 agent 有足够上下文开始工作，不需要回头查任何表。
路由逻辑: 根据 reason 确定 needs_role，查 agent_working 空闲池，分配具体 agent_id。
兜底: reason 无法识别 → needs_agent=manager_01。

所有参数接收方都可用。不需要再回头查 agent_working 或 a2a_tasks。
Manager 收到后判断: 手动处理 / 创建新 issue / 标记 failed / 忽略噪音。

### Card 设计 (agent-roles.toml)

```
docs/system/workspace/agents/agent-roles.toml  ← git tracked, 纯能力声明

[manager]   skills: workflow-guarded-execution, branch-management
[worker]    skills: B1, B2, RED, dev, test
[reviewer]  skills: tdd-review, candidate-acceptance-review

不提 slot，不提 pool。
Slot 在 ACP session 创建时从 agent-table 读取。
```

## 2. 关键决策

| # | 决策 | 理由 |
|---|------|------|
| D1 | Runtime 是 bootstrapper 不是 mediator | A2A 协议原生模式是 agent 直连 |
| D2 | Manager 创建 A2A task，Runtime 只创建 ACP session | Manager 有编排上下文 |
| D3 | 配对靠 raw_key 不靠 NN | 解耦 pool 大小，10 worker + 99 reviewer |
| D4 | agent_working SQLite 替代 agent-id.env | 事务、索引、SQL 查询空闲 |
| D5 | session 嵌在 agent_id 列 (冒号分隔) | 无需额外列，一列同时读 |
| D6 | Reviewer 独立 slot | 可用不同 AI 工具，独立 rate limit |
| D7 | 单文件 agent-roles.toml | 简化维护 |
| D8 | reviewer_id 逗号分隔 (不拆表) | 写入串行，无并发冲突 |
| D9 | 6 种双向 input-required | 无遗漏处理场景 |
| D10 | review_stage 字段 | 区分 b1/b2/dev 审查阶段 |
| D11 | session/fork 同 tool, session/new 跨 tool | 复用连接，减少开销 |
| D12 | SSE 主路径 + 轮询 fallback — SSE 断连时回退到轮询 | 主路径 SSE（push），轮询（pull）降级兜底 |

## 3. TODO List

### P0: Bug Fix
- [ ] P0.1 修 _restore_tasks L403/442/663 and/or 优先级 (加括号)
- [ ] P0.2 修 L442 变量引用 bug (统一用 agent_id)
- [ ] P0.3 reviewer 专属 _restore_tasks 分支 (working + input-required)
- [ ] P0.4 语法 + 逻辑验证

### P1: agent_working 表 + CRUD
- [ ] P1.1 建表 (freely.db migration)
- [ ] P1.2 agent_session_set/get/remove
- [ ] P1.3 agent_working_next(role, pool) / agent_working_free(role, pool)
- [ ] P1.4 agent_working.py 模块 + 单元测试

### P2: agent-table-query 重写
- [ ] P2.1 废弃 --get-reviewer
- [ ] P2.2 --get-slot 适配 v2 格式
- [ ] P2.3 新增 --next-free, --list-role, --pool-size
- [ ] P2.4 更新所有调用方 + 格式验证

### P3: agent-id.env → agent_working 全局替换
- [ ] P3.1 定位所有读写 agent-id.env 位置
- [ ] P3.2 读 → SELECT agent_working
- [ ] P3.3 写 → agent_session_set
- [ ] P3.4 删 → agent_session_remove
- [ ] P3.5 wt-create/wt-close 移除 agent-id.env 逻辑

### P4: ACP Session 管理
- [ ] P4.1 _ensure_reviewer_agent(reviewer_id, parent_worktree)
- [ ] P4.2 ensure_manager_once 写 agent_working
- [ ] P4.3 launch_worker: next_free + agent_session_set
- [ ] P4.4 wt-close: session/close + agent_session_remove + 删除行

### P5: A2A Multi-Card + Task
- [ ] P5.1 agent-card?role= 端点 + agent-roles.toml
- [ ] P5.2 Manager POST /tasks 委派 Worker
- [ ] P5.3 Manager POST /tasks 委派 Reviewer
- [ ] P5.4 PATCH /tasks/{id} SSE 推送 + 订阅过滤
- [ ] P5.5 review_stage 字段 (b1/b2/dev/red/test/gate)
- [ ] P5.6 Worker state 变更 → SSE push (替代轮询)

### P6: Watchdog SSE
- [ ] P6.1 SSE 订阅 + 重连 (exponential backoff)
- [ ] P6.2 needs-review → 创建 Reviewer session
- [ ] P6.3 needs-manager-decision → resume Manager
- [ ] P6.4 needs-worker-retry → resume Worker
- [ ] P6.5 needs-manager-scope → resume Manager
- [ ] P6.6 轮询降级为 30s fallback
- [ ] P6.7 任务僵死检测 (working > N min → stall event)
- [ ] P6.8 SSE 集成测试

### P7: agent-roles.toml
- [ ] P7.1 创建 docs/system/workspace/agents/agent-roles.toml
- [ ] P7.2 三角色 skills 定义
- [ ] P7.3 确认 git tracked (不含 slot/pool)
- [ ] P7.4 agent card 端点读取 agent-roles.toml

### P8: input-required 双向路由 + 兜底
- [ ] P8.1 规范 input-required schema (task_id, from_agent, needs_agent, needs_role, reason, message, raw_key, review_stage, parent_agent, timestamp)
- [ ] P8.2 reason 路由表实现 (6 向匹配 + 兜底 → manager_01)
- [ ] P8.3 needs_agent 分配: 根据 needs_role 查 agent_working 空闲池
- [ ] P8.4 Worker→Reviewer 路由 (needs-review:b1/b2/dev → next_free reviewer)
- [ ] P8.5 Worker→Manager 路由 (needs-manager-decision → manager_01)
- [ ] P8.6 Reviewer→Worker 路由 (needs-worker-retry → from parent_agent)
- [ ] P8.7 Reviewer→Manager 路由 (needs-manager-scope → manager_01)
- [ ] P8.8 Manager→Reviewer 路由 (needs-review:gate/audit → next_free reviewer)
- [ ] P8.9 Manager→Worker 路由 (needs-worker-task → next_free worker)
- [ ] P8.10 message 自动生成 (包含 from_agent, raw_key, review_stage, 产物路径)
- [ ] P8.11 路由验证测试 (6 向 + 兜底 + 未知 reason)

### P9: 生命周期集成
- [ ] P9.1 wt-close: session/close + release + 删行 + 删 worktree
- [ ] P9.2 freely-cycle: dispatch_reviewer 实际执行 (不再只是建议)
- [ ] P9.3 僵死检测 + 孤儿 worktree 清理
- [ ] P9.4 Daemon 重启恢复 agent + SSE 重新订阅

## Candidate

- candidate_id: C-20260701T085407Z-A
- status: promoted
- milestone: M-20260701T085407Z-A
- promoted_issue_id: I-20260701T085407Z-A
- decision_reason: 基于 A2A/ACP 协议 + Zed 参考 + 3 轮 subagent 审查 + 12 项关键决策
- next_action: B2 设计 → 逐 Phase 实现 → PR

## 16. 数据库架构决策 — 复用现有 DB 封装

### 原则：不直接操作 SQLite，走 freely_db_manager daemon

```
所有 DB 操作:
  agent_working.py ──socket RPC──▶ freely_db_manager.py ──sqlite3──▶ freely.db
  a2a_server.py    ──socket RPC──▶ freely_db_manager.py ──sqlite3──▶ freely.db
  freely-db-cli    ──socket RPC──▶ freely_db_manager.py ──sqlite3──▶ freely.db

禁止:
  ❌ sqlite3.connect() 直接打开 freely.db
  ❌ 独立 migration SQL 文件
  ❌ 绕过 DB daemon
```

### agent_working 表创建位置

- **表结构**: `freely_db_manager.py._ensure_tables()` (与 chats, sessions, a2a_tasks 并列)
- **索引**: 同上，`CREATE INDEX IF NOT EXISTS`
- **Schema migration**: 同上，`ALTER TABLE ... ADD COLUMN` (review_stage)
- **CRUD**: `agent_working.py` 通过 `_db_rpc()` socket 调用

### 已有 DB 基础设施

| 组件 | 职责 |
|------|------|
| `freely_db_manager.py` | DB daemon，管理所有表，监听 Unix socket |
| `freely-db-cli` | CLI 客户端，`python3 freely-db-cli --project ... table.action` |
| `a2a_task.py` | A2A task 专用 CLI |
| `SQLiteTaskStore (a2a_server.py)` | A2A server 内部使用的 task store |

agent_working 复用 `_db_rpc()` 模式（与 `SQLiteTaskStore._db_rpc()` 一致）。

## 17. Agent 协作核心流程（Freely 能力基础）

### 类比：subagent 委派模式

```
主管 (Manager) 委派任务给下属 (Worker)，下属做完汇报。
主管审阅结果，必要时请审查员 (Reviewer) 把关，再决定下一步。

Freely 多了一层 ACP（AI CLI 工具给 agent 装大脑），
以及 A2A (SSE) 作为 agent 之间的通信总线。
```

### 完整时序

```
Runtime      ACP          a2a_tasks      Manager        Worker         Reviewer
(Watchdog)   (AI能力)     (状态账本)     (develop)      (fix wt)       (develop/test)
    │           │             │              │              │              │
    │──ACP session/new──────▶│              │              │              │
    │  "你是 Manager"        │              │              │              │
    │           │             │              │──patrol scan▶│              │
    │           │             │              │ 发现待办 issue│              │
    │           │             │              │              │              │
    │           │             │              │──A2A task──▶ │              │
    │           │             │              │ POST /tasks  │              │
    │           │             │              │ role=worker  │              │
    │           │             │              │ skill=B1     │              │
    │           │             │              │              │              │
    │──ACP session/new──────▶│              │              │              │
    │  "你是 Worker"         │              │              │              │
    │           │             │              │              │──B1 skill──▶ │
    │           │             │              │              │ working      │
    │           │             │◀──PATCH──────│              │              │
    │           │             │ state=input- │              │              │
    │           │             │ required     │              │              │
    │           │             │ reason=needs-│              │              │
    │           │             │ review:b1    │              │              │
    │           │             │              │              │              │
    │           │             │──SSE push──▶ │              │              │
    │           │             │              │              │              │
    │◀──SSE subscribe─────────│              │              │              │
    │  detect: needs-review   │              │              │              │
    │           │             │              │              │              │
    │──ACP session/new──────▶│              │              │              │
    │  "你是 Reviewer"        │              │              │              │
    │           │             │              │              │              │
    │           │             │              │──A2A task──▶ │              │──review────▶
    │           │             │              │ role=reviewer│              │ working      │
    │           │             │              │              │              │
    │           │             │◀──PATCH──────│              │              │──verdict────▶
    │           │             │ state=completed            │              │ pass/fail    │
    │           │             │ verdict=pass               │              │              │
    │           │             │              │              │              │
    │           │             │──SSE push──▶ │              │              │
    │           │             │              │              │              │
    │           │             │              │──处理结果──▶ │              │
    │           │             │              │ verdict=pass │              │
    │           │             │              │ → 继续 B2    │──B2 skill──▶ │
    │           │             │              │              │              │
```

### 三个 Agent 的职责与通信

```
Manager (develop):
  职责: 巡逻、委派、收口
  启动: Runtime ACP session/new
  通信: 通过 A2A POST /tasks 委派 Worker/Reviewer
       通过 A2A SSE 接收 Worker/Reviewer 状态变更
       通过 ACP session/prompt 处理复杂决策

Worker (fix/raw-{key}):
  职责: 执行 skill (B1/B2/RED/dev/test)
  启动: Manager 委派后 Runtime ACP session/new
  通信: 通过 A2A PATCH /tasks/{id} 更新状态
       通过 A2A SSE 接收 Reviewer verdict
       完成时设 input-required → Manager 收到

Reviewer (test-pre-merge-{key} 或 develop):
  职责: 审查 Worker 产物，给出 verdict
  启动: Runtime Watchdog 检测到 needs-review 后 ACP session/new
  通信: 通过 A2A PATCH /tasks/{id} 写 verdict
       通过 A2A SSE 推送 verdict 给 Manager + Worker
```

### 关键通信路径

| 场景 | 通信方式 | 说明 |
|------|---------|------|
| Manager 委派 Worker | A2A POST /tasks | "你去做 B1" |
| Worker 报告完成 | A2A PATCH state=input-required | "我做完了，请审查" |
| Worker 通知 Manager | A2A SSE → Manager | 实时推送 |
| Runtime 启动 Reviewer | ACP session/new | "你需要审查这个" |
| Reviewer 给出结论 | A2A PATCH state=completed | "通过，继续" 或 "不通过，重做" |
| Reviewer 通知 Worker | A2A SSE → Worker | 实时推送 verdict |
| Manager 决定下一步 | ACP session/prompt | AI 决策：继续/重做/停止 |

### 与 subagent 委派的类比

```
人类主管委派 subagent:
  主管: "审查一下这个 PR"
  subagent: 审查 → "通过，没有发现问题"
  主管: 收到结果 → merge

Freely 的等价:
  Manager (ACP): 通过 A2A POST /tasks 委派 Reviewer
  Reviewer (ACP): 审查 → A2A PATCH state=completed, verdict=pass
  Manager: 通过 A2A SSE 收到 → ACP session/prompt 决策 → 告诉 Worker 继续
```

## 18. B2 实现后反向更新（Implementation Reconciliation）

此章节在 B2 实现完成后写入，记录设计文档与实际实现之间的差异，
确保 B1 设计文档与最终代码一致，避免后续读者困惑。

> 更新日期: 2026-07-02
> 来源: 3 轮 subagent 审查 + 连通性审计 + 73 测试 + 69 commits
> 审查文档: review-01~09 (docs/B2-docs/.../code-reviews/)

### 18.1 SSE 事件格式（设计 vs 实现）

**B1 设计**（§1 reason vs message）:
```json
{"statusUpdate": {"status": {"state": "input-required"}, "metadata": {...}}}
```
A2A TaskStatusUpdateEvent 标准嵌套格式。

**实际实现**:
```json
{"task_id": "...", "state": "input-required", "reason": "needs-review:b1", ...}
```
平铺格式。`_notify_sse()` 直接构造 `{task_id, state, ...fields}`，不套 `statusUpdate`。

**原因**: A2A `_notify_sse` 是内部函数，不经过完整 A2A protocol buffer 序列化。
PATCH handler 直接将 whitelisted fields 传给 SSE subscribers。
`watchdog_sse.py._handle_sse_event()` 相应地解析平铺格式。

**影响**: §1 的 "A2A 协议对齐" 表格（`status.message → message`, `metadata → reason`）仅适用于完整 A2A 协议路径。
内部 SSE 推送走简化格式。两者在 `_notify_sse` 层面统一。

### 18.2 SSE 全局流端点

**B1 设计**（§5 A2A Multi-Card + Task）:
仅提到 per-task SSE stream (`/tasks/{id}/stream`)，用于单 task 订阅。

**实际实现**:
新增了 `GET /tasks/stream` 全局 SSE 端点（`_global_task_stream_endpoint`）。
所有 task 的 state 变更都推送到此流。watchdog 订阅全局流而非逐 task 订阅。

**原因**: per-task stream 要求 watchdog 提前知道所有 task_id，无法处理"新 task 动态出现"的场景。
全局流让 watchdog 只需维护一个 SSE 连接即可监听所有 agent 的 input-required 事件。

### 18.3 双看门狗架构

**B1 设计**（§1 Runtime Watchdog = Bootstrapper）:
只描述了一个 Runtime Watchdog，负责检测 needs-review + 创建 ACP session。

**实际实现**:
两个看门狗并行运行：
- **Shell watchdog** (`sse-watchdog.sh`): 轮询 A2A tasks，更新 agent_working，兼容存量
- **Python watchdog** (`watchdog_sse.py`): 事件驱动，订阅全局 SSE 流，处理 input-required 路由 + ACP session 创建 + liveness/staleness 检测

**启动**: `launch_sse_watchdog()` 同时启动两者。Python watchdog 通过 socket timeout (30s) 在 SSE 活跃期间运行定时检查。

### 18.4 agent_get_session 多 Reviewer 处理

**B1 设计**（§1 agent_working 表）:
`reviewer_id` 列格式: `reviewer_05:ses_ghi,reviewer_08:ses_jkl`（逗号分隔多对）。
未指定如何从多 reviewer 中取 session_id。

**实际实现**:
`h_aw_get_session` 逻辑:
- 有 `agent_id` 参数: 解析逗号分隔 pairs，返回匹配的 session_id
- 无 `agent_id` 参数: 返回第一个 reviewer 的 session_id（`next(iter(pairs.values()))`)
- 修复了原 `split(":",1)[1]` 在逗号分隔字符串上返回垃圾的 bug

### 18.5 ACP session 关闭双函数

**B1 设计**（§1 ACP vs A2A）:
只提到 `session/close`，未区分使用场景。

**实际实现**:
两个函数，不同签名和使用场景：
- `_acp_session_close(project, session_id)`: 直接按 session_id 关闭。用于 ACP bridge 重启路径（bridge 切换时关闭旧 session）
- `_acp_agent_session_close(project, role, raw_key)`: 从 agent_working 查 session_id 再关闭。用于 wt-close 路径

函数重命名历史: 原始 `_acp_session_close` → 错误地重命名为 `_acp_agent_session_close`（签名变化导致 bridge 重启路径调用未定义函数）→ 恢复 `_acp_session_close` 并保留 `_acp_agent_session_close`

### 18.6 TOCTOU 防护: 原子 next_free_and_assign

**B1 设计**（§1 agent_working 表 + TODO P1.3）:
`agent_working_next(role, pool)` + `agent_working_free(role, pool)` 两个独立操作。

**实际实现**:
新增 `agent_working.next_free_and_assign` RPC handler（原子操作）:
1. 计算空闲 agent_id
2. 在同一 RPC 内完成 INSERT/UPDATE
3. 消除 `next_free` → `assign` 之间的 TOCTOU 窗口

原有的 `agent_next_free` + `agent_assign` 仍然保留（用于需要分步检查的场景）。

### 18.7 freely-cycle 注入防护

**B1 设计**:
未涉及 freely-cycle 的实现细节。

**实际实现**:
`bin/freely-cycle` 中的 dispatch_reviewer 逻辑原本使用 f-string 将 `raw_key`/`project` 直接插值进 Python 代码。
修复后使用环境变量 `FREELY_RAW_KEY`/`FREELY_PROJECT` 传递数据，消除注入风险。

### 18.8 SQL 注入防护

**B1 设计**:
未涉及 DB handler 防御细节。

**实际实现**:
`freely_db_manager.py` 中的 `@_h` handler 新增列名验证：
- `h_aw_upsert`: `col` 参数必须匹配 `^(manager|worker|reviewer)_id$`
- `h_aw_get_session` / `h_aw_next_free`: `role` 参数必须为 `manager|worker|reviewer`
- 防止通过构造恶意 col/role 参数注入 SQL

### 18.9 _restore_tasks: 从日志到实际恢复

**B1 设计**（§1 Daemon 重启 → resume）:
daemon 重启时恢复 agent session。

**实际实现**:
- D5: 新增 `_aw_resume_script` 模块级常量（Python inline script），扫描 agent_working 表
  中所有带 session_id 的条目，通过 ACP bridge socket 逐个调用 `session/resume`
- D6: 推送 `restore_complete` SSE 事件（is_global=True），通知所有 subscriber
- 原设计只有 "Daemon 重启 → resume" 一句话，实现补充了完整的恢复链路

### 18.10 PATCH handler 字段白名单

**B1 设计**（§1 input-required 事件完整参数）:
定义了 15+ 字段的完整事件参数（task_id, from_agent, from_role, needs_agent, needs_role, raw_key, reason, review_stage, skill, message, parent_agent, session_id, timestamp）。

**实际实现**:
`a2a_server.py` PATCH handler 白名单:
```
completion_summary, evidence_paths, error, reason, next_action, progress,
summary, next, evidence, session_id, from_agent, needs_agent, needs_role,
raw_key, review_stage
```

并非所有 B1 设计的字段都在白名单中。`from_role`、`skill`、`parent_agent`、`timestamp` 不在 PATCH 白名单中——它们通过其他途径传递（A2A task 的 agent_id 字段推断 role，skill 在 task 创建时设置，timestamp 由 a2a_tasks 的 created_at/updated_at 提供）。

### 18.11 消息自动生成（未实现）

**B1 设计**（§1 message 自动生成）:
```
"agent 设 input-required 时不手写 message。Runtime 根据参数自动生成：
 {from_agent} 在 raw_key={raw_key} 完成 {review_stage}，需要 {reason}。
 产物路径: docs/B2-docs/{epic}/{story}/raw-{raw_key}/..."
```

**实际状态**: 此功能尚未实现。message 字段通过 PATCH handler 的 `message` 参数手动传入。
自动生成逻辑待后续版本添加。

**影响**: 当前依赖 agent 手动填写 message。如果 agent 未填写，接收方 agent 需要从其他字段（raw_key + reason + review_stage）推断上下文。

### 18.12 设计决策 D12（轮询降级）的澄清

**B1 D12**: "轮询降级为 SSE fallback"

**实际实现**:
- 主路径是 `watchdog_sse.py` 订阅 A2A SSE 全局流（push 模式）
- Fallback 是 `bin/freely-cycle --all`（pull 模式，Manager daemon 每 N 秒轮询一次）
- D12 原文措辞有歧义——"轮询降级为 SSE fallback" 暗示 SSE 是 fallback
- 实际是 **SSE 主路径，轮询降级**（即"SSE 为主，轮询为 fallback"）
- 更正: 主路径 SSE，断连时回退到轮询

### 18.13 双工位模型（dev + test-pre-merge）

**B1 设计**（§1 三角色 + Worktree 绑定）:
Reviewer 绑定到 test-pre-merge-{key} 工位。

**实际实现**:
wt-close 的 test-pre-merge cleanup (Phase 6b) 通过 raw_key 自动发现 companion test worktree:
- 从 `fix/raw-{key}-{slug}` 推导 `test-pre-merge-{key}-{slug}`
- 删除前先关闭 ACP session（所有角色）
- 释放 agent_working 表条目
- 删除 worktree + branch

审查者工位与开发工位共享 raw_key，通过分支命名约定关联（无需存储关系）。

### 18.14 设计文档一致性自检

| 检查项 | B1 设计 | 实现 | 状态 |
|--------|---------|------|------|
| agent_working 表结构 | raw_key PK, 6 列 + timestamps | 同设计 | ✅ 一致 |
| agent_working 值格式 | agent_id:session_id | 同设计 | ✅ 一致 |
| reviewer 逗号分隔 | 多对逗号分隔 | 同设计 + 修复 get_session bug | ✅ 一致 |
| InputRequiredReason Enum | 12 值 (含 UNKNOWN) | 同设计 | ✅ 一致 |
| 6 向路由 | 完整路由表 | 同设计 | ✅ 一致 |
| agent-roles.toml | git tracked, 不提 slot/pool | 同设计 | ✅ 一致 |
| agent-table.toml v2 | 扁平格式, role 字段 | 同设计 | ✅ 一致 |
| SSE 事件格式 | statusUpdate 嵌套 | 平铺格式 | ⚠️ 已更新（见 §18.1） |
| SSE 全局流 | 未提及 | 已实现 | ⚠️ 已更新（见 §18.2） |
| 双看门狗 | 单一 Watchdog | Shell + Python 并行 | ⚠️ 已更新（见 §18.3） |
| message 自动生成 | Runtime 自动生成 | 未实现（agent 手动填写） | ⚠️ 待实现 |
| 轮询降级 | "轮询降级为 SSE fallback" | SSE 主路径，轮询为 fallback | ⚠️ 已更正（见 §18.12） |
| ACP session 关闭 | 单一 session/close | 双函数（直接/agent_working） | ⚠️ 已更新（见 §18.5） |
| 原子分配 | 未提及 | next_free_and_assign | ⚠️ 新增（见 §18.6） |
| SQL 注入防护 | 未提及 | col/role 验证 | ⚠️ 新增（见 §18.8） |
| Reviewer session 复用 | 未涉及 | 见 §19 | ⚠️ 新增（见 §19） |

## 19. Reviewer Session 复用策略（2026-07-02 研究）

### 问题

当前 `_handle_needs_reviewer` 对每次 needs-review 都调用 `_acp_session_new`。
即使同一 raw_key 的 B1→B2→RED→dev→test 连续多轮审查，每次都启动全新 session，
每次冷启动都要重新加载 CONSTITUTION、LAWS、代码库上下文。大量 token 浪费。

另一方面，如果直接 fork Worker 的 session，Reviewer 会继承 Worker 的完整对话历史——
包括 Worker 的实现思路、决策过程、踩坑记录。这会导致"自己审自己"的偏见：
Reviewer 看到 Worker 是怎么想的，很难保持独立判断。

### 业界研究

**Claude Code 内部**：
- Fork：继承父 session 的 system prompt + tools + conversation history → 首轮命中缓存
- Subagent：独立 system prompt + 独立 context window → 冷启动，但完全隔离
- Anthropic 刻意将两者分开："fork 用于 compaction（缓存优先），subagent 用于 review（隔离优先）"

**Qwen Code**：
- Named subagent：干净 context + 自定义 system prompt → 适合专项任务
- Fork subagent：继承父 context + 80% token 节省 → 适合并行探索

**ttal 多 agent 系统**：
- Brainstorm → Fork → Plan → Review 四阶段模式
- Fork 从同一个 master session 分叉出多个 project-specific session
- 保持上下文共享的同时做到 scope 隔离

**关键发现**：业界共识是 fork Manager session 是效率与公平的最佳平衡点。
Manager 有项目治理上下文（CONSTITUTION/LAWS/代码库结构），但没有 Worker 的实现细节。
Fork Manager 出来的 Reviewer 继承了"审查所需的上下文"但不继承"被审查者的思路"。

### 设计决策

```
Reviewer dispatch session 选择决策树:

1. 同一 raw_key 之前审查过？
   ├─ YES + session 存活 (agent_working 有 session_id)
   │   → session/resume
   │   Cache: ⭐⭐⭐ (完整审查历史)  Impartial: ⭐⭐⭐
   │   例子: Reviewer 审了 B1，现在审 B2，直接在同一对话继续
   │
   └─ YES + session 已死 → 进入步骤 2

2. Manager 与 Reviewer 是否同 AI tool？
   ├─ YES → session/fork from Manager ← 默认首选
   │   Cache: ⭐⭐ (Manager 有项目宪法+代码库，≈80% token 节省)
   │   Impartial: ⭐⭐⭐ (Manager 是中立角色，无 Worker 偏见)
   │
   └─ NO (跨 tool) → session/new
       Cache: ⭐ (完全冷启动)
       Impartial: ⭐⭐⭐

3. 是否是 Gate 审查 (needs-review:gate)？
   └─ → session/new 始终
       理由: Gate 是最关键的放行节点，值得付出冷启动成本换最大化公正性
```

### session/fork from Manager 为什么是安全的

```
Manager session 包含:
  ✅ CONSTITUTION.md, LAWS.md, PROJECT_INTENT.md (治理上下文)
  ✅ 代码库结构理解 (directory tree，关键文件位置)
  ✅ 项目历史上下文 (之前处理过的 issue)
  ✅ Skill 指令定义

Manager session 不包含:
  ❌ Worker 的具体实现代码 (Worker 在自己工位，Manager 在 develop)
  ❌ Worker 的推理过程 (Worker 有自己的 ACP session，不共享)
  ❌ Worker 的踩坑记录
  ❌ Worker 的自我评估

→ Fork Manager 出来的 Reviewer 有足够的上下文开始审查，
   但没有 Worker 的"作案思路"，能保持独立判断。
```

### session/fork from Worker 为什么必须禁止

```
Worker session 包含:
  ❌ 实现思路和决策过程 ("我选择方案A因为...")
  ❌ 中途的自我怀疑和修正 ("等等，这里可能有问题...让我改一下")
  ❌ 对测试结果的解释 ("这个失败是环境问题，不是代码bug")
  ❌ 对自己的代码的正面评价 ("这个实现很优雅")

→ Fork Worker 出来的 Reviewer 会被这些信息影响判断。
   人类代码审查时也不会先让作者讲一遍思路再审查。
```

### 实现计划

1. **新增 `_acp_session_fork()`**（freely 脚本 + watchdog_sse.py）
   - 通过 ACP bridge 发送 `session/fork` RPC
   - 参数: parent_role (manager), child_role (reviewer), parent_session_id, raw_key

2. **修改 `_handle_needs_reviewer()` 决策树**
   - 步骤 1: 查 agent_working → 有 session_id → session/resume
   - 步骤 2: 判断同 tool → session/fork from Manager
   - 步骤 3: 跨 tool 或 gate → session/new

3. **agent_working 记录 session_mode**
   - 新增字段: `reviewer_session_mode` (fork|resume|new)
   - 或在现有列值中追加模式标记: `reviewer_05:ses_abc:fork`

4. **Gate 审查特殊处理**
   - `needs-review:gate` → 强制 session/new（即使缓存可用）
   - 在 agent_working 标记 `force_new=true`

### 预期效果

| 场景 | 当前 (always new) | 优化后 | 节省 |
|------|------------------|--------|------|
| B1 审查 (首次) | session/new (cold) | session/fork (Manager cache) | ~80% |
| B2 审查 (同 raw_key) | session/new (cold) | session/resume (reviewer cache) | ~90% |
| RED 审查 | session/new (cold) | session/resume | ~90% |
| dev 审查 | session/new (cold) | session/resume | ~90% |
| test 审查 | session/new (cold) | session/resume | ~90% |
| Gate 审查 | session/new | session/new (故意保留) | 0% (公正优先) |
| 跨 tool 审查 | session/new | session/new (被迫) | 0% |

同一 raw_key 的生命周期内（B1→B2→RED→dev→test→gate），
原来需要 6 次 cold start，优化后只需 1 次 fork + 4 次 resume + 1 次 new (gate)。

### 实现后修正（2026-07-02，基于实际码码审查）

**Session 存活模型（纠正此前误解）**：

ACP bridge 的 `ACP_IDLE_TIMEOUT = 180s` **只在 `session/prompt` 调用期间检测 AI 响应性**，
不在两次调用之间杀 session。Worker 完成 B1 后 session 进入空闲等待，不会被 timeout 杀掉。
session 持久存活直到主动 `session/close` 或 freely stop 清理。

**Agent 间消息投递机制**：

`session/resume` + `prompt` 参数 = 一次性「唤醒 session + 投递消息」。
不阻塞等待 AI 完成，只等 resume 确认即返回。ACP bridge 透传 prompt 到 AI CLI tool。

**ACP / A2A 分工最终确认**：

```
A2A = 信号系统                  ACP = 对话系统
PATCH task state                session/new|fork|resume  启停对话
SSE push 实时通知                session/resume + prompt  投递消息
a2a_tasks 表持久落盘             session/prompt           语义封装
                                session/close            关闭对话

串联: Agent 完成阶段 → A2A SSE 发出信号 → watchdog 消费 →
      ACP 启动/投递到目标 agent → agent 工作 → Skill 指令约束交接 →
      A2A SSE 发出下一轮信号 → 闭环
```

**Handler 决策树（实现后）**：

三个 handler 统一为: alive? → `_acp_session_prompt` → dead? → fork/new + prompt
- Reviewer: 首次 fork from Manager，后续 resume+prompt（同 raw_key 连续审查）
- Worker: 活 session prompt，死 session fork/new + prompt（verdict 在 prompt 里）
- Manager: 活 session prompt，死 session new + prompt

**关键修复记录**：

- Phase 1: Bridge `session/resume` 原丢弃 prompt 参数 → 修复透传
- Phase 2: Handler 统一 session/prompt 优先 + session 创建后立即投递任务
- Review bugfix: `_handle_needs_reviewer` prompt 失败后漏 return → 会分配第二个 reviewer
- Review bugfix: `_build_worker_verdict_message` metadata 参数未使用 → 提取 verdict/summary
- **`__manager__`**：Manager 硬编码 raw_key，与 issue raw_key 分离。`_should_use_fork` 和 `_acp_session_fork` 查 `__manager__` 而不是 issue key
- **`update_only`**：Reviewer 只能 UPDATE 已有行（Worker 创建），不允许 INSERT。防止 worktree 已被 wt-close 删后 Reviewer 误创建幽灵行

