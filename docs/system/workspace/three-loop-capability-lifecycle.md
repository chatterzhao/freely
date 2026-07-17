# Three-Loop Capability Lifecycle

本文件是 Freely 能力生命周期路由的唯一细节真源。SVG 图为视觉总览，本文为文字规范。

> **AI 入口指引**：`AGENTS.md` §规范流程 提供了面向 AI agent 和用户的标准操作链路（feat/fix/doc-only 三种变体）。本文为底层真源，AGENTS.md 为上层入口。

![Three-Loop Lifecycle](three-loop-lifecycle.svg)

凡是会改变 three-loop routing、loop placement、completion / verification / cleanup / recovery judgment 的实现、prompt、agent、skill 或高层文档，在修改前都必须先阅读并理解本文件；若语义变化，必须同步更新本文件及 SVG 图。

## 五层架构

SVG 图展示的五层实体，从上到下、从内到外：

| 层 | 实体 | 框型 | 说明 |
|----|------|------|------|
| **Layer 1** | Freely Runtime-managed boundary | 虚线大框 | supervisor + managed daemons 的系统边界，不等于单一进程 |
| **Layer 2** | auto-loop / doc-loop / dev-loop | 实线泳道 / gate | lifecycle workflow surface，表达阶段、gate 和回环，不是进程 |
| **Layer 3** | Manager Agent / Worker Agent / Reviewer Agent | 虚线框 | prompt-defined AI role，由下方 AI provider 的 ACP session 执行；不是独立进程 |
| **Layer 3a** | M-Skills / W-Skills | 点线框 | instruction / capability modules，被 Manager / Worker role 选择和消费；不是 Actor |
| **Layer 4** | ACP Bridge / A2A Server / freely-db daemon / SQLite-WAL | 服务框 + 存储框 | ACP Bridge/A2A Server/freely-db daemon 是服务/守护进程；SQLite/WAL 是 durable datastore 文件 |
| **Layer 5** | AI provider / AI CLI tool (Claude Code/codex/opencode/...) | 外部进程框 | 外部 AI 执行提供层；Freely 通过 ACP 对其发 prompt、resume/fork session 并接收 stopReason |

### 实体框型约定

- **外层虚线大框** = runtime-managed boundary：Freely supervisor 管理的系统边界。
- **带标题条实线框** = 真实进程或守护进程（有 PID，可启停）：ACP Bridge, A2A Server, freely-db daemon, AI provider / AI CLI Tool。
- **泳道 / gate 实线框** = workflow surface：auto/doc/dev loop 的阶段与判断点，不表示进程。
- **虚线角色框** = AI role：Manager Agent / Worker Agent，由 prompt、上下文和 skill 约束定义，在 AI provider session 中执行。
- **点线框** = instruction/capability module set：M-Skills, W-Skills。
- **SQLite/WAL 存储框** = durable datastore 文件，不单独拥有 PID；由 `freely_db_manager.py` 持有单 SQLite connection 并通过 Unix socket JSON-RPC 读写。

### 协议通道

- **ACP (AI Communication Protocol)**：Freely runtime/ACP bridge 与外部 AI provider 之间的 session/prompt/control protocol，不是 Agent 间协商协议。它负责 session/new、session/resume、fork/prompt、stopReason、session/ping 等；当前产品工作模式是 ACP。Freely 通过 `monitor-ai-acp.sh` → `run-acp-prompt.py` → `acp-bridge.py` 连接外部 AI CLI 的 ACP server。canonical ACP family 当前是 `claude-agent-acp`、`codex-acp`、`opencode acp`；`cc` / `kiro-cli` / `iflow` 等 legacy 名称按 registry alias 进入 Claude ACP family。
    **故障检测分层** (#3301/#3303):
    - **Layer 1 (通用)**: idle timeout / network failure / quota exhausted — 所有工具生效。idle timeout 默认 180s，超时后不重试，直接触发 auto-recovery。
    - **Layer 2 (工具专属)**: codex rate-limit / kiro monthly-limit — 按工具注册的故障模式。
- **A2A (Agent-to-Agent Protocol)**：Manager / Worker / Reviewer 三角色之间的 task coordination / state / notification protocol。A2A Server 是 coordination service；`a2a_task.py` / `a2a-exit` 是 CLI client/tool。Manager 用 `a2a-exit --state submitted --role worker` 创建 Worker Task（**必须用 `--role worker`，不能使用已废弃的 `--agent-id worker`**，否则 Task 会以默认 `agent_id=manager` 创建，Runtime 无法发现）。Runtime 通过 `list --role worker --status submitted` 发现 pending Task → 生成 Worker prompt file → ACP Bridge 启动独立 Worker ACP session。Worker 完成后调用 `a2a-exit --state completed` 或 PATCH `state=input-required`（携带 `reason` Enum 值触发 Reviewer 路由）→ A2A task state 更新 + `_notify_sse()` 推送到全局流 (`GET /tasks/stream`) + 按 task_id 推送到单 task subscriber。watchdog_sse.py 订阅全局流，按 `InputRequiredReason` 枚举值路由到 Manager/Worker/Reviewer。旧 `handoffs` 文件/表语义已被 `a2a_tasks` 取代。

### SQLite 表职责

SQLite 不是单一职责的 crash-recovery 文件；不同表在 Freely runtime 中承担不同职责：

| 表 | 职责 |
|----|------|
| `a2a_tasks` | Manager/Worker 委派、状态机、Task.message、worker delivery/consumption |
| `chats` | human interruption / chat intake 暂存与消费状态 |
| `sessions` | ACP session、tool adapter、launch_kind、父子 session 关系 |
| `tool_failure_log` / `tool_switch_events` | tool availability、slot-first recovery、跨工具切换证据 |
| `task_mode_gate` | `auto` / `wait` / `listen` 模式门控 |
| `agent_working` | agent-worktree-session 绑定（替代 agent-id.env）。raw_key 为主键，manager_id/worker_id/reviewer_id 列存 `agent_id:session_id` 格式。reviewer 逗号分隔多对 |

### 关键数据流

```
scan (文件系统读取) ──→ intake gate ──→ routing ──→ dispatch
                                                      │
                              ┌────────────────────────┘
                              ▼
              Manager ACP session → AI 决策 → a2a-exit --state submitted --role worker
                                                      │
                              ┌────────────────────────┘
                              ▼
              A2A Server: a2a_tasks 存储 (agent_id=worker, state=submitted)
                              │
                              ▼
              Runtime Task Launcher: list --role worker --status submitted
                              │
                              ├── 生成 Worker prompt file (task-{id}.txt)
                              ├── ACP Bridge → session/new → 启动 Worker ACP session
                              └── 更新 task state: submitted → working (launched)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
        doc-loop Worker                  dev-loop Worker
        (B1_IBM→B2_IBM)                 (implement→evidence)
              │                               │
              └───────────┬───────────────────┘
                          ▼
              a2a-exit --state completed   OR   PATCH state=input-required (reason=needs-review:*)
                          │                                    │
                          ▼                                    ▼
              SSE → Manager 下一轮 patrol        SSE global stream → watchdog_sse.py
                                                    │
                                                    ├─ InputRequiredReason 路由 (6向+兜底)
                                                    ├─ agent_working.next_free → Reviewer 分配
                                                    ├─ session/fork from Manager (继承治理上下文)
                                                    └─ session/prompt → Reviewer 收到审查任务
                                                        │
                                                        ▼
                                              Reviewer 审查 → PATCH verdict (pass/fail)
                                                        │
                                              pass? → SSE → Manager/Worker 继续
                                              fail? → needs-worker-retry → Worker 重做

Manager 是常驻 session，Runtime 通过 session/prompt 驱动每轮 patrol。
a2a-exit 提交本轮决策后回到守候，进程不休。

Manager 决策出口（manager_exit_contract_kind）:
  - delegate_workers: Worker 已委派到 A2A Server，Runtime 负责启动 Worker
  - manager_working:  Worker 已派出/容量满，保持 session 继续等待
  - resume_manager:   Manager 需要继续分析（B1 评估、复杂决策）
  - stop_ai:          无事可做，暂停 patrol，等下一轮唤醒。**严禁连续 stop_ai**
```

## 三 Loop 架构

| Loop | 驱动源 | 角色 | 核心职责 |
|------|--------|------|---------|
| **auto-loop (L3)** | task-mode (auto/wait/listen) → scan + A2A SSE + continuity evidence | Manager + Runtime Watchdog | 信号接收 → 路由分发 → gate 序列 → Reviewer 调度 → 收口 |
| **doc-loop (L1)** | auto-loop dispatch gate → 委派 Worker → Reviewer 审查 | Worker + Reviewer | B1_IBM (预研) → Reviewer → B2_IBM (设计) → Reviewer |
| **dev-loop (L2)** | auto-loop dispatch gate → 委派 Worker → Reviewer 审查 | Worker + Reviewer | RED → Reviewer → dev → Reviewer → test-GREEN → Reviewer |

auto-loop 是唯一的调度中枢。doc-loop 和 dev-loop 不自行启动，始终由 auto-loop 的 dispatch gate 触发。
每阶段完成后通过 A2A SSE (input-required + reason Enum) 触发 Reviewer 审查，
审查通过后返回继续下一阶段，完成后返回 auto-loop 继续下一 gate。

## auto-loop（主管调度层）

### Gate 序列

```
intake → routing → dispatch → test → pr-create → pr-review → CI check → pr-merge → closeout
  ↻                       ↻        ↻          ↻           ↻          ↻            ↻
```

每个 gate 内部都有小循环（↻）：失败 → 回修 → 重试。

### 各 gate 详细说明

#### intake gate（阶段1）
- 触发: scan 有新 item / chat 插话 / 平台发现新 issue
- 执行: `freely task-source-scan` 读取 standing-source inventory
- 输出: 待处理 items 列表
- 命令封装: 由 freely runtime 自动执行，无需手动调用

#### routing gate（阶段2-3）
- 触发: intake 有新 item 需要创建工位
- 执行: `freely feedback` → 创建 raw issue → GitHub 平台
- 继续: `wt-create --raw-key <key> --source <source> --skill <skill> --slug <slug>`
- 命令封装: `wt-create` 内部自动执行 `git fetch origin develop` + `git update-ref` + `git worktree add` + test-pre-merge worktree 创建

#### dispatch gate（阶段4-6 入口）
- 触发: scan items 的 `next_action` 字段
- 执行: Manager 读取 next_action → 判断 [manager] wt-create 或 [worker] delegate
- 路由: 向 doc-loop 或 dev-loop 委派 Worker
- 顺序: B1→B2→dev 是串行的（先 doc-loop 后 dev-loop）
- **委派前检查**: `a2a_task.py list --raw-key <key> --status working,submitted` 防重复委派 (#3285)
- **三种 dispatch 模式** (#3286):
  - **委派**: `a2a-exit --state submitted --role worker --summary "..."` (新任务)
  - **纠偏**: `a2a_task.py prompt --task-id <id> --message "..."` (Worker 活着，调整方向)
  - **重试**: `a2a_task.py update --task-id <id> --state submitted` (Worker 死了，重新启动)

**Worker 委派协议（a2a-exit 接口约定）**：
- Manager 必须使用 `a2a-exit --state submitted --role worker --worktree <path> --branch <name> --raw-key <key> --summary "完整指令"`
- **禁止使用 `--agent-id` 参数**（该参数已被 `--role` 取代，使用 `--agent-id worker` 会导致 task 以默认 `agent_id=manager` 创建，Runtime 无法发现，`worker_prompts_csv=none`）
- Runtime Task Launcher 通过 `list --role worker --status submitted` 发现 pending Worker task
- 发现后：生成 prompt file → 更新 task state 为 working → ACP Bridge 启动独立 Worker ACP session
- Worker 完成后：`a2a-exit --state completed` → A2A task state 更新 → SSE 通知 Manager

**Worker A2A Task 状态机**：
```
submitted ──→ working (launched) ──→ completed
     │              │                    │
     └──────────────┴────────────────────┘
                    ↓
              failed / input-required / pending-input
```
- `submitted`: Manager 已委派，等待 Runtime Task Launcher 启动
- `working`: Worker ACP session 已启动
- `completed`: Worker 正常完成
- `failed`: Worker 异常退出
- `input-required`: Worker/Manager/Reviewer 需要其他 agent 介入。携带 `reason` 字段（InputRequiredReason Enum，12值），通过 A2A SSE 全局流推送到 watchdog_sse.py，按 `needs_role` 路由到 Manager/Worker/Reviewer，触发 ACP session/new 或 session/resume
- `pending-input`: 等待外部输入（human interruption 等）

#### test gate（阶段7）
- 触发: dev-loop 返回 evidence 就绪
- 执行: 将来源 `feature/*` / `fix/*` 临时装配到 `test-pre-merge-{key}-{slug}` worktree → 端到端验证
- 内部小循环: fail → back to source branch dev-loop fix → 重新装配测试工位 → re-test → pass
- 注意: `test-pre-merge-*` 是一次性测试沙箱，只用于临时验证；验证后丢弃，不作为合并来源。验证通过后仍由来源分支走 `pr-create-guarded` / `pr-review-guarded` / `pr-merge-guarded develop <source-branch>`。

#### pr-create gate（阶段8）
- 触发: test gate 通过
- 执行: `pr-create-guarded`
- 命令封装: `pr-create-guarded` 内部执行 `git pull origin develop` + `pr-merge-guarded --dry-run` + `git push` + `gh pr create`
- 内部小循环: conflict → 解决 → re-pull; gate fail → back to dev-loop fix

#### pr-review gate（阶段9）
- 触发: PR 已创建
- 执行: `pr-review-guarded` → 6 维独立 review → verdict 文档 (pass/fail)
- 命令封装: `pr-review-guarded` 内部从 correctness / security / performance / reuse / governance / testing 六个维度审查 diff，产出 verdict 文档
- 内部小循环: verdict=fail → back to dev-loop fix; 不通过 review 不得进入 CI

#### CI check gate（阶段10）
- 触发: pr-review gate 通过 (verdict=pass)
- 执行: CI (`pr-merge-guard.yml`) + 人 review → Approval
- 位置: 外部（GitHub），不在 Freely runtime 内

#### pr-merge gate（阶段11）
- 触发: PR 获得 Approval
- 执行: `pr-merge-guarded develop <pr-branch>`
- 命令封装: `pr-merge-guarded` 内部执行 `git fetch origin develop` + PR gate (check PR + approval) + promotion gate + `git merge --no-ff` + issue-sync + `develop-push`
- 内部小循环: gate fail → back to dev-loop fix

#### closeout gate（阶段12）
- 触发: merge 完成
- 执行: `wt-close <branch>`
- 命令封装: `wt-close` 内部执行 Phase 1-3 (phase_state check + platform close + force-close trace) → Phase 4 (delete remote branch) → Phase 4.5 (Worker 安全下线: 查询活跃 Worker → session/prompt 通知 → kill) → Phase 5 (auto-consume A2A → worktree remove → branch -d)
- 注意: `pr-merge-guarded` 不再删除远程分支 (#3280)。远程分支删除统一由 `wt-close` 负责。
- 完成后: 回到 intake gate，开始下一轮 scan

## doc-loop（文档设计层）

```
auto-loop dispatch gate 触发
  │
  ├── B1_IBM (阶段4)
  │   └── brainstorm → converge → candidate → promote/absorb/drop
  │       ↻ 边界未稳 → 继续 brainstorm
  │
  └── B2_IBM (阶段5)
      └── I-* → prd.md → pre-tests.md → tasks.md → code-reviews/
          ↻ 设计未 ready → 继续设计
      
完成后返回 auto-loop dispatch gate（判断进入 dev-loop）
```

触发命令: `skill:freely-doc-B1_IBM-execution` / `skill:freely-doc-B2_IBM-execution`

## dev-loop（开发实现层）

```
auto-loop dispatch gate 触发
  │
  ├── implement (阶段6)
  │   └── 写代码 → feature-local 测试
  │       ↻ fail → fix → re-test
  │
  └── evidence (阶段6)
      └── progress → code-review → implementation decision note
          ↻ 证据不足 → 补充

完成后返回 auto-loop test gate
```

触发命令: `skill:freely-dev-loop-execution`

## 完整管线（feedback → wt-close）在三 loop 中的流转

```
阶段:  |  1-3   |   4-5   |    6    |    7    |    8    |     9     |   10    |   11   |  12
loop:  | auto   |  doc    |   dev   |  auto   |  auto   |   auto    | external| auto   | auto
gate:  |intake  | B1→B2   |implem→  |  test   |pr-create| pr-review | CI check|pr-merge|closeout
       |routing |         |evidence |         |         |           |         |        |

auto:  intake → routing → dispatch ──→ test → pr-create → pr-review → [CI check] → pr-merge → closeout
                 │           │           │                              ↑
doc:             │    B1→B2  │           │                              │
dev:             │           └── implement→evidence ────────────────────┘
```

## 命令封装一览

所有 gate 命令均为封装接口，接收参数，内部自动执行多步操作。

| 命令 | 内部步骤 |
|------|---------|
| `freely feedback --repo <repo> --title "..." --body "..."` | 在 GitHub 创建 raw issue（raw issue 不存在时需要） |
| `wt-create --raw-key <key> --source platform --skill <skill> --slug <slug>` | `git fetch origin develop` → `git update-ref` → `git worktree add` → test-pre-merge worktree → raw-issue-pull → platform_ids fill |
| `pr-create-guarded` | `git pull origin develop` → `pr-merge-guarded --dry-run` → `git push origin HEAD` → `platform-adapter create-pr` |
| `pr-review-guarded` | 6 维独立 review (correctness / security / performance / reuse / governance / testing) → verdict 文档 (pass/fail) |
| `pr-merge-guarded develop <pr-branch>` | `git fetch origin develop` → validate direction → PR gate (check PR + approval) → promotion gate → `git merge --no-ff` → issue-sync → `develop-push` → `platform-adapter close-pr` |
| `wt-close <branch>` | Phase 1-3 (phase_state check + platform close) → Phase 4 (delete remote branch) → Phase 4.5 (Worker shutdown) → Phase 5 (auto-consume A2A → worktree remove → branch -d) |

## 变体路径

### Fix 修复（治理先行，与 feature 完全一致）
```
[cmd] freely feedback → [skill] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close
```

### Hotfix 紧急修复
```
从 main 创建 hotfix/*，走完整流程（同上），唯一区别：合并目标为 main + develop
（与 fix 流程完全一致，唯一区别：合并目标为 main + develop）
```

### Doc-only 纯文档
```
[cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close
（跳过 B1、B2。test 不可跳过，即使是纯文档也必须验证）
```

## Runtime 监督面机制真源（2026-07-17 与实现对齐）

本章镜像 `docs/system/workspace/scripts/runtime/freely` 的现行监督机制。修改这些机制的 lane 必须同步本章。

### Supervisor 存活检测：heartbeat（替代已废除的 L220-L240 grace chain）

- supervisor 启动后（信号 trap 安装后、doc gate / bridge init 之前）立即同步 touch `.freely/run/supervisor-heartbeat` 并启动后台子进程每 2s 续 touch；子进程以 `kill -0 父进程` 自检，父死自灭
- `ensure-manager` 以 heartbeat mtime 判活：超时 `SUPERVISOR_HEARTBEAT_TIMEOUT_SECS`（默认 120s）
- **新生宽限**：heartbeat 文件缺失，或其 mtime 早于 `supervisor.pid`（上代遗留），以 supervisor 自身出生时间起算宽限 `SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS`（默认 15s），绝不因上代 stale 债处决新生 supervisor
- 判死动作走 `restart_manager_supervisor_preserving_handoff`（TERM→等待→KILL 兜底）并以 `kill -0` 验证消亡后才重拉；不可杀时记 `manager_watchdog_supervisor_kill_failed` 并跳过本 tick（防双 daemon）——daemon supervisor 有意忽略无 stop-marker 的裸 TERM（operator-stop 区分，raw-20260711T100936Z）
- supervisor 的 EXIT trap 为单一合并 handler（heartbeat 子进程回收 + cleanup_supervisor）；bash 同信号 trap 后写覆盖前写，禁止再加第二条 `trap ... EXIT`

### ACP Bridge 生命周期（lazy-start / warmup / 回收 / idle-sleep / auto-wake）

- daemon 启动只 eager 启动 manager base_tool 的 bridge；worker/reviewer 工具在首次委派时 auto-wake（`_sync_project_tooling`）
- 主循环 per-cycle ensure 带 **lazy-start 守卫**：非 manager 且无 pid 文件（未被 auto-wake 启动过）的工具跳过，不 eager 重生
- 复用判定顺序：bin 变更→重启；base tool 变更→重启；同 tool→健康检查（5s socket initialize 探针，bridge 从缓存应答）；健康检查失败但 bridge 龄 < `ACP_BRIDGE_WARMUP_GRACE_SECS`（默认 20s）→ warming 复用（ACP server 冷启动 ~8s）
- 判定需重生时，先 `terminate_pid_with_graceful_wait` 回收存活旧 pid 再删跟踪文件（防孤儿泄漏）
- bridge 自身 idle 监视：`ACP_IDLE_TIMEOUT`（180s）+ `ACP_IDLE_SHUTDOWN_GRACE`（30s）＝约 210s 无活动自关（有活跃 session/prompt 时跳过）

### task_mode 三态语义（daemon 运行模式；与 AI_MODE 区分）

| 模式 | 主循环行为 |
|------|-----------|
| `auto` | 全功能：scan → prompt build（A-L020）→ AI launch → patrol |
| `wait` | `sleep CHECK_INTERVAL(10s) + continue`——**跳过 prompt build 与 AI launch**，静默轮询 |
| `listen` | 每轮仅 scan；发现 ready item **自动切回 auto**；否则 sleep `LISTEN_INTERVAL`(300s) |
| `id:<scan-id>` | 单任务过滤 |

`AI_MODE`（交互姿态，auto/step，默认 auto）与 `task_mode`（默认 wait）是两个独立轴（raw-20260715T063959Z）。daemon start 未显式传 `--task-mode` 时为 wait——不启动 AI 是设计内行为。

### Restart storm / churn 观测（现行阈值）

- 窗口 `RESTART_STORM_WINDOW_SECS=120`，计数阈值 `RESTART_STORM_COUNT=10`，进程峰值阈值 `PROCESS_CHURN_PEAK=3`（计数口径 supervisor+dispatcher+ai，上限 3）
- 记录点：AI 周期完成处（kind=cycle）+ **ensure-manager 侧 supervisor 死亡/teardown/非 operator 重拉处**（kind=death，`record_supervisor_death_for_storm_window`）。peak 仅统计 death 行——cycle 行不计峰（健康态恒 3 会误触,raw-20260717T090202Z 自查修正）
- 阈值命中 → `record_restart_storm_signal` → manager bootstrap handoff + `restart_storm_supervisor_churn_signal` 事件；信号 advisory，terminal judgement 归 manager（watchdog-control-plane 契约）

### Loop Guard（L0-L3 防呆层）

- L0：fresh launch storm（`LOOP_GUARD_L0_WINDOW_SECS=300` 内 fresh 启动 ≥`LOOP_GUARD_L0_FRESH_THRESHOLD=3`）
- L1：action 指纹停滞；L2：token 浪费；L3：硬预算上限
- 详见 runtime 源码 `_loop_guard_*`；命中动作为 task_mode 门控切换，不直接杀进程
