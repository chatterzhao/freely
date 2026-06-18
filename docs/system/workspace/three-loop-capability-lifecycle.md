# Three-Loop Capability Lifecycle

本文件是 Freely 能力生命周期路由的唯一细节真源。SVG 图为视觉总览，本文为文字规范。

> **AI 入口指引**：`AGENTS.md` §规范流程 提供了面向 AI agent 和用户的标准操作链路（feat/fix/doc-only 三种变体）。本文为底层真源，AGENTS.md 为上层入口。

![Three-Loop Lifecycle](three-loop-lifecycle.svg)

凡是会改变 three-loop routing、loop placement、completion / verification / cleanup / recovery judgment 的实现、prompt、agent、skill 或高层文档，在修改前都必须先阅读并理解本文件；若语义变化，必须同步更新本文件及 SVG 图。

## 五层架构

SVG 图展示的五层实体，从上到下、从内到外：

| 层 | 实体 | 框型 | 说明 |
|----|------|------|------|
| **Layer 1** | Freely Runtime | 实线大框 | bash supervisor, while-true loop, 最外层容器 |
| **Layer 2** | auto-loop / doc-loop / dev-loop | 实线泳道 | 三个 Loop 的 gate 序列和逻辑流程 |
| **Layer 3** | Manager Agent / Worker Agent | 虚线框 | 逻辑角色（非独立进程），由 prompt 注入定义 |
| **Layer 3a** | M-Skills / W-Skills | 点线框 | Skill 集合，按 Manager / Worker / 通用能力被 Agent 消费 |
| **Layer 4** | ACP Bridge / A2A Server / DB daemon + SQLite/WAL | 实线框 | 真实进程通过 Unix socket 通信；SQLite/WAL 是持久化文件，不是进程 |
| **Layer 5** | AI CLI Tool (Claude Code/codex/opencode/...) | 实线框 | 外部独立进程，在 Runtime 之外，通过 ACP JSON-RPC 连接 |

### 实体框型约定

- **实线框** = 真实进程或守护进程（有 PID，可启停）：Freely Runtime, ACP Bridge, A2A Server, DB daemon, AI CLI Tool
- **虚线框** = 逻辑角色（AI Agent，由 prompt 注入定义）：Manager Agent, Worker Agent
- **点线框** = Skill 集合：M-Skills, W-Skills
- **DB 文件** = SQLite/WAL 持久化，不单独拥有 PID；由 `freely_db_manager.py` 通过 Unix socket 对外提供 JSON-RPC。

### 协议通道

- **ACP (AI Communication Protocol)**：当前默认工作模式。Freely Runtime 通过 `monitor-ai-acp.sh` → `run-acp-prompt.py` → `acp-bridge.py` 连接外部 AI CLI 的 ACP server。canonical ACP family 当前是 `claude-agent-acp`、`codex-acp`、`opencode acp`；`cc` / `kiro-cli` / `iflow` 等 legacy 名称按 registry alias 进入 Claude ACP family。session/new → session/resume → session/prompt → stopReason。三级缓存：L1 resume (0 token) | L2 fork (增量) | L3 fresh (全量)
- **A2A (Agent-to-Agent Protocol)**：REST + SSE over Unix socket。Manager ↔ Worker 之间的零文件委派。a2a-exit → Task.message → tasks/list → Worker prompt → SSE TaskStatusUpdateEvent。旧 `handoffs` 文件/表语义已被 `a2a_tasks` 取代。

### SQLite 表职责

SQLite 不是单一职责的 crash-recovery 文件；不同表在 Freely runtime 中承担不同职责：

| 表 | 职责 |
|----|------|
| `a2a_tasks` | Manager/Worker 委派、状态机、Task.message、worker delivery/consumption |
| `chats` | human interruption / chat intake 暂存与消费状态 |
| `sessions` | ACP session、tool adapter、launch_kind、父子 session 关系 |
| `tool_failure_log` / `tool_switch_events` | tool availability、slot-first recovery、跨工具切换证据 |
| `task_mode_gate` | `auto` / `wait` / `listen` 模式门控 |

### 关键数据流

```
scan (文件系统读取) ──→ intake gate ──→ routing ──→ dispatch
                                                      │
                              ┌────────────────────────┘
                              ▼
              Manager ACP session → AI 决策 → a2a-exit --state submitted
                                                      │
                              ┌────────────────────────┘
                              ▼
              A2A Server: a2a_tasks 存储 → SSE 通知
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
        doc-loop Worker                  dev-loop Worker
        (B1_IBM→B2_IBM)                 (implement→evidence)
              │                               │
              └───────────┬───────────────────┘
                          ▼
              a2a-exit --state completed
                          │
                          ▼
              SSE → Manager 下一轮 patrol → test gate → ... → closeout
```

## 三 Loop 架构

| Loop | 驱动源 | 角色 | 核心职责 |
|------|--------|------|---------|
| **auto-loop** | task-mode (auto/wait/listen) → scan + A2A/continuity evidence | 主管 (Manager) | 信号接收 → 路由分发 → gate 序列 → 收口 |
| **doc-loop** | auto-loop dispatch gate → 委派 Worker | Worker | B1_IBM (预研) → B2_IBM (设计) |
| **dev-loop** | auto-loop dispatch gate → 委派 Worker | Worker | 实现 → 测试 → 证据 |

auto-loop 是唯一的调度中枢。doc-loop 和 dev-loop 不自行启动，始终由 auto-loop 的 dispatch gate 触发，完成后返回 auto-loop 继续下一 gate。

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
- 命令封装: `wt-close` 内部执行 issue-sync close + milestone update + `git branch -d` + `git push --delete` + worktree remove
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
| `wt-create --raw-key <key> --source <source> --skill <skill> --slug <slug>` | `git fetch origin develop` → `git update-ref` → `git worktree add` → test-pre-merge worktree → raw-issue-pull → platform_ids fill |
| `pr-create-guarded` | `git pull origin develop` → `pr-merge-guarded --dry-run` → `git push origin HEAD` → `gh pr create --head HEAD` |
| `pr-review-guarded` | 6 维独立 review (correctness / security / performance / reuse / governance / testing) → verdict 文档 (pass/fail) |
| `pr-merge-guarded develop <pr-branch>` | `git fetch origin develop` → validate direction → PR gate (check PR + approval) → promotion gate → `git merge --no-ff` → issue-sync → `develop-push` |
| `wt-close <branch>` | issue-sync close → milestone update → `git branch -d` → `git push --delete` → worktree remove |

## 变体路径

### Fix 修复（治理后置）
```
wt-create → dev(implement) → test → B1 → B2 → pr-create → pr-review → pr-merge → wt-close
                                   ↑ B1/B2 后置于 test 之后，PR 门禁不后置
```

### Hotfix 紧急修复
```
从 main 创建 hotfix/* → dev → pr-create → pr-review → pr-merge main → pr-merge develop → wt-close
（可跳过 test-pre-merge，双合并 main+develop）
```

### Doc-only 纯文档
```
dev → pr-create → pr-review → pr-merge → wt-close
（跳过 test-pre-merge、B1、B2）
```
