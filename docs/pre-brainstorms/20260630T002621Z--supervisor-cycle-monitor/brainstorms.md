---
b1_id: B1-20260630T002621Z
phase_state: completed
source_raw: raw-20260630T002621Z
source_url: https://github.com/chatterzhao/freely/issues/3638
produced_candidate: C-20260630T002621Z-A
created_at: 2026-06-30
---

# B1_IBM: 主管持续监督与中途介入

## Input
- 来源：GitHub #3638 raw-20260630T002621Z
- kind：feature（新能力，非 bug 修复）
- 触发：本轮会话连续 6 个 PR 中，Worker RED 阶段全部糊弄（actual_RED_output = "code written before RED" × N），Manager 完全不知情

## Discovery

### 现有能力盘点

**已有（可复用）：**
- A2A Server + a2a_tasks 表：task 状态机 submitted → working → input-required → working → ... → completed / failed / canceled
- a2a_task.py CLI：list（按 raw_key/status 过滤）、prompt（往 worker session 发消息）、update（改状态）
- ACP session/fork：reviewer 可 fork manager session 命中缓存
- agent-table.toml：已注册 reviewer 角色和 slot
- wt-close Phase 4.5：关工位前停 worker 进程、关 ACP session
- three-loop lifecycle：Layer 1 定义 supervisor 管理边界

**缺失（需要新增）：**
- Manager 侧无周期轮询 Worker 过程的能力
- Worker 的 ACP session transcript 没有被 Manager 消费
- 无阶段识别（不知道 Worker 当前在 B1/B2/RED/dev/GREEN 哪一步）
- 无质量检查点（RED 的 actual_RED_output 是否有意义？evidence_file 是否真实？）
- 无中途介入路径（只能等 Worker 完成或 kill 进程）

**限制条件：**
- Worker 在 dedicated worktree 中运行，有自己的 .freely/ 状态
- ACP session/fork 可以共享缓存，但 Worker session 是 session/new（独立上下文）
- GitHub 网络当前不可达（影响 remote call 类方案）
- Manager 和 Worker 运行在同一台机器，不是分布式

### 对标分析

**Agent Conveyor（Codex CLI）**
- Manager 调 `conveyor cycle <task>` 读取 Worker 的 JSONL rollout + tmux 截图
- 返回结构化 JSON：新事件数、Worker 状态、建议动作
- Manager 决定 continue / nudge / interrupt / finish
- 关键：**Manager 读文件而非等通知**——主动拉取

**CAO（AWS Labs）**
- tmux capture buffer 检测状态：IDLE/PROCESSING/COMPLETED/WAITING_USER_ANSWER/ERROR
- assign（非阻塞委托）+ send_message（inbox 回传）+ handoff（阻塞转移）
- 关键：**状态机驱动 + inbox 异步消息**

**Superharness**
- heartbeat 事件驱动（非轮询），stall detection
- auto-approve safe operations，auto-respawn crashed workers
- 关键：**事件驱动而非轮询，降低 overhead**

**与 Freely 的差异**

| 维度 | Conveyor | Freely 现状 | Freely 目标 |
|------|---------|------------|-----------|
| 通信协议 | 自定义 CLI + tmux | ACP + A2A | ACP + A2A + cycle |
| 过程可见性 | JSONL rollout 持续可读 | 仅 final handoff | cycle 读 transcript |
| 阶段感知 | 无（通用监督） | 无 | 识别 B1/B2/RED/dev/GREEN |
| 介入方式 | session-nudge（tmux send-keys） | a2a_task.py prompt | 复用 a2a prompt + 新增质量告警 |
| 并发 | 一个 binding 一个 worker | 支持多 worker | 多 worker 并行监督 |
| 缓存 | 无（独立 tmux session） | session/fork 可命中 | Worker session 独立，Reviewer session 可 fork |

## Problem

**核心问题**：Manager 是"收件人"不是"旁观者"。

```
现状时序:
  Manager                    Worker                 Reviewer
    │                          │                       │
    │── submitted ────────────→│                       │
    │                          │ B1                    │
    │         （看不见）         │ B2                    │
    │         （看不见）         │ RED ← 糊弄了           │
    │         （看不见）         │ dev                   │
    │         （看不见）         │ GREEN                 │
    │←── completed ────────────│                       │
    │                          │                       │
    │ pr-review-guarded ──────────────────────────────→│ ← 太晚了
    │                          │                       │
```

**三个具体危害：**

1. **RED 形同虚设**：Worker 先写代码再补 pre-tests，actual_RED_output 全填 "code written before RED"。Manager 不知道，reviewer 到 PR 阶段才发现——但代码都写完了。

2. **GREEN ghost pass**：evidence_file 是一行 "GREEN: PASS"，无实际命令输出。Manager 不知道，reviewer 到 PR 阶段才发现——但已经 commit 了。

3. **阶段跳跃**：Worker 跳过 B2 直接写代码，跳过 test-GREEN 直接 PR。Manager 不知道——handoff 说 "done"。

## Brainstorm

### Option A: 轮询 ACP transcript（近似 Conveyor cycle）

Manager 周期调用 `freely cycle --raw-key <key>`：
- 读 Worker 的 ACP session transcript（通过 ACP bridge API）
- 解析最近 N 条消息，识别阶段标记
- 检查关键字段质量（actual_RED_output 是否占位符？evidence_file 是否真实？）
- 返回 JSON：阶段、状态、质量评分、建议动作

**优点**：最接近 Conveyor 模式，实时性高
**缺点**：依赖 ACP bridge API 稳定暴露 transcript；轮询 overhead

### Option B: 文件驱动的检查点（Superharness heartbeat 风格）

Worker 在每个阶段完成时写入检查点文件（`.freely/run/phase-checkpoint.json`）。Manager 的 watchdog 进程监听文件变更事件（inotify/fswatch），发现新检查点时触发质量检查。

**优点**：事件驱动无轮询 overhead；检查点文件是持久证据
**缺点**：Worker 需要配合写检查点——但如果 Worker 本身在糊弄，检查点也可以糊弄

### Option C: A2A message 流 + SSE 推送

Worker 在关键节点通过 a2a_task.py add-message 发送进度消息。Manager 通过 SSE 订阅实时收到。Manager 根据消息内容决定是否介入。

**优点**：基于现有 A2A + SSE 基础设施；推送而非轮询
**缺点**：Worker 需要主动报告——糊弄的 Worker 不会报告自己糊弄

### Option D: 混合方案（Cycle + Checkpoint + A2A message）

```
Layer 1: Manager watchdog 进程
  └── 周期性 cycle 轮询（读 ACP transcript + a2a message 历史）
  └── 阶段识别 + 质量检查规则引擎
  └── 告警 → a2a prompt nudge / escalation / kill

Layer 2: Worker 被动配合
  └── 正常运行，不要求主动报告
  └── ACP transcript 自动记录所有操作（Manager 旁观）

Layer 3: Reviewer agent
  └── fork manager session，读 cycle 累积证据
  └── 关键节点独立评审（RED 后、GREEN 后）
```

**优点**：Manager 旁观不依赖 Worker 配合，Reviewer 独立评审，多层防护
**缺点**：实现量大，需要分阶段交付

## Decision: Option D — 分 Phase 交付

### Phase 1: Manager cycle + Reviewer 语义审核（本 candidate 范围）

实现三件事：

**1. `freely cycle --raw-key <key>`**
- Manager 的轮询入口
- 检测 a2a state=input-required → 触发 review dispatch
- 检测超时 → 告警
- 检测 completed → wt-close
- **不做 phase 检测**——那是 Reviewer 的事

**2. Reviewer 语义审核**
- Fork Manager session（缓存命中）
- 收到 review 任务（phase=X）后：
  - 检查所有前置 phase 是否按顺序真实完成（读文件内容 + git log）
  - 检查当前 phase 产出质量（不是文件存在性——是内容质量）
  - 判断 IBM skip 是否合法
- 直接对 Worker 发 GO/FIX（a2a prompt + state=working）
- 向 Manager 回报 verdict

**3. Worker HALT 协议**
- 每 phase = 一个 ACP prompt
- Prompt 结束 → a2a state=input-required → Worker 空闲
- Manager 不发下一 prompt → Worker 不可能继续
- Reviewer GO/FIX 是下一个 prompt

**不做的（Phase 2/3）**：
- 自动 dispatch reviewer（Phase 1 Manager 手动 trigger cycle）
- 多 worker 并发
- Reviewer fork+review 全自动化

## 深入预研：四个关键技术问题

### Q1: 如何跨 AI CLI tool 读 Worker session 数据

不同 AI CLI tool 的 session 数据格式和访问方式不同：

| Tool | Session 存储 | 读取方式 |
|------|-------------|---------|
| Claude Code (cc) | ACP bridge socket `/tmp/freely-acp-*.sock` | `session/prompt` 注入"汇报当前阶段"提示词，读回文本 |
| Codex | `~/.codex/sessions/<id>/rollout-*.jsonl` | 直接读 JSONL 文件 |
| OpenCode | ACP bridge (opencode acp) | 同 cc |
| Kiro | ACP bridge | 同 cc |

需要 **SessionReader 抽象层**：

```
SessionReader
├── ACPReader        ← cc, opencode, kiro
│   └── session/prompt注入"__freely_phase_report__" → 解析返回文本
├── CodexReader      ← codex
│   └── 读 rollout JSONL → 提取最近 N 条 message
└── FallbackReader   ← 其他
    └── 读 a2a_task message 历史（Worker 主动上报）
```

ACP 路径下没有 `session/read` 端点——不能直接读 transcript。替代方案：
1. **注入探针 prompt**：`session/prompt` 发一条 `"__FREELY_CYCLE__ 报告你当前的工作阶段和最新产出"`。Worker session 收到后会在回复中说明状态。
2. **文件旁路**：如果 ACP bridge 把 transcript 落盘（JSONL），直接读文件。
3. **Worker 主动上报**：Worker 在阶段完成时通过 `a2a_task.py add-message` 写入结构化状态。

推荐方案：**ACP 探针注入 + a2a message 历史兜底**。ACP 路径下用探针 prompt，非 ACP 路径下读文件。

### Q2: ACP 能映射 Conveyor 的四种介入类型吗

Conveyor 的四种介入：

| Conveyor | 含义 | Freely ACP 等价 | 实现方式 |
|----------|------|----------------|---------|
| `continue` | 一切正常，继续 | `continue` | cycle 返回 `suggested_action: "continue"`，Manager 不做任何操作 |
| `nudge` | 轻推，给个提示 | `session/prompt` 注入提示消息 | `a2a_task.py prompt --task-id <id> --message "提示"` → Worker session 收到 |
| `interrupt` | 中断当前工作，注入新指令 | `session/prompt` + Worker 侧配合 | Manager 发 `session/prompt` 注入中断指令 → Worker 下次 tool call 时看到 → 停止当前任务执行新指令 |
| `finish` | 终止 worker | `session/close` + a2a state=completed/canceled | Manager 调 `a2a_task.py update --task-id <id> --state canceled` |

**关键差异**：Conveyor 的 `interrupt` 是通过 tmux Ctrl-C 真正打断进程。ACP 的 `session/prompt` 是**协作式**的——Worker 要在下一个 tool call 时才看到新消息。如果 Worker 正在执行长时间 tool call（如 `bash` 跑测试），`session/prompt` 不能中断它。

**解决方案**：
- 对 ACP 工具：`session/prompt` 注入 `__FREELY_INTERRUPT__` 标记 + 在 Worker agent prompt 中约定"每轮开始先检查是否有 interrupt 消息"
- 对 Codex：`kill -INT <pid>` + `codex exec --resume <session>` 重新注入上下文
- 通用：Manager 可以 `kill` worker 进程 + `a2a_task update --state blocked` + 写 blocker reason

### Q3: 不同 tool 的介入命令差异如何抹平

需要 **InterventionAdapter** 抽象：

```
InterventionAdapter
├── nudge(session_id, message)   → tool 特定的"发消息"方式
├── interrupt(session_id, reason) → tool 特定的"中断"方式
├── finish(task_id, reason)      → 通用 A2A state update
└── get_status(session_id)       → tool 特定的"读状态"方式

Per-tool 实现:
  cc:     nudge → session/prompt,  interrupt → session/prompt + worker prompt 约定
  codex:  nudge → codex exec --session <id> "message", interrupt → kill + resume
  kiro:   nudge → session/prompt,  interrupt → session/prompt + worker prompt 约定
```

### Q4: 卡点-评审-继续 模式

用户的核心设计：**Manager 是红绿灯，不是交警**。

```
每个 workflow 阶段完成后 → Worker STOP → Manager cycle 发现 → Manager 派 Reviewer → Reviewer 独立评审 → verdict → Worker 继续/返工

时序:

Manager                    Worker                    Reviewer
  │                         │                         │
  │── submitted ───────────→│                         │
  │                         │ B1 done ──→ HALT        │
  │← cycle: phase=B1 ───────│                         │
  │                         │                         │
  │── a2a prompt: "STOP" ─→│                         │
  │                         │ (等待)                   │
  │── dispatch review ──────────────────────────────→│ fork manager session
  │                         │                         │ read B1 artifacts
  │←── verdict: pass ───────────────────────────────│
  │                         │                         │
  │── a2a prompt: "GO" ──→│                         │
  │                         │ B2 + pre-tests → HALT   │
  │← cycle: phase=B2 ───────│                         │
  │── a2a prompt: "STOP" ─→│                         │
  │── dispatch review ──────────────────────────────→│ fork, read pre-tests
  │←── verdict: FAIL ───────────────────────────────│
  │── a2a prompt: "FIX:..." ─→│                      │
  │                         │ RED 重做 → HALT         │
  │← cycle: phase=RED ──────│                         │
  │── dispatch review ──────────────────────────────→│ fork, check actual_RED
  │←── verdict: pass ───────────────────────────────│
  │── a2a prompt: "GO" ──→│                         │
  ...                      ...                       ...
```

**Manager 职责**：
1. 轮询 cycle，检测阶段完成
2. 发 STOP 指令，Worker 等待
3. 派 Reviewer（A2A dispatch）
4. 收 verdict，转发给 Worker（GO / FIX）
5. 继续 cycle 轮询

**Reviewer 职责**：
1. Fork manager session（缓存命中）
2. 读当前阶段产物（brainstorms / pre-tests / actual_RED_output / evidence）
3. 独立评审，不参考 Worker 的"我做了"自述
4. 返回结构化 verdict

**Worker 职责**：
1. 执行 workflow 阶段
2. 阶段完成时主动 HALT（不再推进）
3. 等待 Manager 的 GO/FIX 指令
4. 收到 FIX 时根据 reviewer 反馈修改
5. 收到 GO 时继续下一阶段

**卡点位置**（每个阶段后）：

| 卡点 | Review 内容 |  Reviewer 关注 |
|------|-----------|---------------|
| B1 后 | brainstorms.md, candidates.md | 方案是否充分？根因是否正确？ |
| B2 后 | pre-tests.md, tasks.md | test_command 是否真实？expected_output 是否具体？ |
| RED 后 | actual_RED_output, red_how | 是否真的执行了 RED？输出是否占位符？ |
| dev 后 | code diff, implementation decision | 实现是否匹配 B2 设计？ |
| GREEN 后 | actual_output, evidence_file | 是否逐条执行？evidence 是否真实？ |

**Manager 不需要懂业务**——它只需要识别阶段标记 + 派 reviewer。Reviewer fork 了 Manager 的 session 上下文（有项目知识和治理规则），独立判断。

## 深入预研（续）：职责边界与命令归属

### Q5: "暂停" 在不同 AI CLI tool 上的实现

用户类比：TUI 里按 ESC 打断 AI。ACP 创建的 session，不同工具是否都能"暂停"？

**现状**：ACP 协议没有 `session/cancel` 端点。`session/prompt` 是追加消息，不打断当前 generation。

**方案**：不在协议层暂停——在 **Worker agent prompt 约定** 层实现。

Worker 的 agent prompt 中注入约定：

```
## Freely Supervisor Protocol

每个 workflow 阶段完成后，你必须：
1. 调用 a2a-exit --state blocked --reason "phase: <B1|B2|RED|dev|GREEN> done, waiting review"
2. 等待 Manager 的 GO 信号后再继续下一阶段
3. 每轮对话开始时，先检查 a2a task 状态是否变为 working（GO 信号）
```

Manager 的"暂停"实际上是：
1. Worker 主动在阶段边界 HALT（通过 a2a state=input-required）
2. Manager 检测到 blocked → 派 Reviewer
3. Reviewer 评审完后 → `a2a_task.py update --state working` + `a2a_task.py prompt --message "GO: continue to <next-phase>"` → Worker 恢复

**Per-tool 配置**：在 `tool-registry.toml` 中注册：

```toml
[tool.codex]
interrupt_method = "a2a_state_blocked"    # 通过 A2A state 控制
resume_method = "a2a_state_working"       # 恢复：改 state + prompt
session_probe = "a2a_message_poll"        # 读状态：查 a2a message

[tool.cc]
interrupt_method = "a2a_state_blocked"
resume_method = "a2a_state_working"
session_probe = "acp_prompt_inject"       # 读状态：ACP 探针注入
```

Freely 代码读配置，按 tool 类型执行对应的 interrupt/resume/probe 方法。

### Q6: Reviewer 直接对 Worker 发指令，还是经 Manager 转发

**决策**：Reviewer 直接对 Worker 发指令。

```
时序:

Manager                    Worker                    Reviewer
  │                         │                         │
  │← cycle: phase=RED ─────│ RED done → a2a blocked   │
  │                         │                         │
  │── dispatch review ──────────────────────────────→│ fork, read artifacts
  │                         │                         │
  │                         │←── a2a prompt: "RED     │ 直接发给 Worker
  │                         │    failed, actual_RED   │
  │                         │    is placeholder.      │
  │                         │    Redo RED with real   │
  │                         │    test execution."     │
  │                         │                         │
  │                         │←── a2a state: working ──│ 恢复 Worker
  │                         │                         │
  │←── verdict: fail ───────────────────────────────│ 只报结果
  │    "reviewer_NN told                              │
  │     worker_NN to redo RED"                        │
  │                         │                         │
  │ (继续 cycle 监控)        │ RED 重做中...            │
```

**理由**：
- 减少一跳延迟（Reviewer → Manager → Worker 变成 Reviewer → Worker）
- Manager 不需要理解业务细节（"RED 为什么失败"的修复建议由 Reviewer 直接给）
- Manager 只需要知道状态：哪个 worker 在哪个阶段、被谁 review 了、verdict 是什么

**Manager 收到的 verdict 报告格式**：

```json
{
  "verdict": "fail",
  "phase": "RED",
  "worker": "worker_03",
  "reviewer": "reviewer_03",
  "action_taken": "direct_fix_assigned",
  "summary": "actual_RED_output is placeholder. Told worker_03 to redo RED with real test execution.",
  "expected_next_phase": "RED"
}
```

### Q7: pr-create/merge/close 的归属

当前命令归属：

| 命令 | 当前执行者 | 工位 | 问题 |
|------|----------|------|------|
| `pr-create-guarded` | Worker | fix|feature worktree | ✅ |
| `pr-review-guarded` | Worker/Manager | develop worktree | ⚠️ ACP reviewer 不可用，且与 checkpoint reviewer 重叠 |
| `pr-merge-guarded` | Worker | develop worktree | ❌ Worker 不应该操作 develop |
| `wt-close` | Worker | develop worktree | ❌ Worker 不应该操作 develop |

**重新划分**：

```
Worker 工位（fix|feature worktree）:
  B1 → B2 → RED → dev → GREEN → pr-create-guarded
  （所有阶段在自己的 fix|feature worktree 完成）

Manager 工位（develop worktree）:
  pr-merge-guarded develop <branch>
  wt-close --raw-key <key>
  （只有 Manager 能操作 develop）

Reviewer（fork Manager session，独立 ACP session）:
  每阶段卡点评审
  pr-create 后最终评审（替代 pr-review-guarded）
```

**pr-review-guarded 的命运**：

有了 per-phase checkpoint reviewer，pr-review-guarded 的 6 维 review 变成冗余：
- RED 维度 → RED checkpoint reviewer 已查
- GREEN 维度 → GREEN checkpoint reviewer 已查
- adequacy 维度 → B2 checkpoint reviewer 已查
- refactor 维度 → dev checkpoint reviewer 已查

**替代方案**：pr-create-guarded 成功后自动触发最终 reviewer（汇总之前所有阶段的 verdict），全部 pass 则允许 merge。不再需要独立的 pr-review-guarded 命令。

**pr-merge-guarded**：Manager 在 develop worktree 执行。命令不变。

**wt-close**：Manager 在 develop worktree 执行。命令不变（`--raw-key` 已支持）。

### 修正后的全流程时序

```
manager_01 (develop wt)       worker_NN (fix|feature wt)    reviewer_NN (fork manager_01)
  │                             │                            │
  │── a2a submitted ──────────→│                            │
  │                             │                            │
  │← cycle: phase=B1 ─────────│ B1 → a2a blocked           │
  │── dispatch ───────────────────────────────────────────→│
  │                             │←── GO/FIX ───────────────│
  │← verdict ─────────────────────────────────────────────│
  │                             │ B2 → a2a blocked           │
  │← cycle: phase=B2 ─────────│                            │
  │── dispatch ───────────────────────────────────────────→│
  │                             │←── GO/FIX ───────────────│
  │← verdict ─────────────────────────────────────────────│
  │                             │ RED → a2a blocked          │
  │← cycle: phase=RED ─────────│                            │
  │── dispatch ───────────────────────────────────────────→│
  │                             │←── GO/FIX ───────────────│
  │← verdict ─────────────────────────────────────────────│
  │                             │ dev → a2a blocked          │
  │← cycle: phase=dev ─────────│                            │
  │── dispatch ───────────────────────────────────────────→│
  │                             │←── GO/FIX ───────────────│
  │← verdict ─────────────────────────────────────────────│
  │                             │ GREEN → a2a blocked        │
  │← cycle: phase=GREEN ───────│                            │
  │── dispatch ───────────────────────────────────────────→│
  │                             │←── GO/FIX ───────────────│
  │← verdict ─────────────────────────────────────────────│
  │                             │ pr-create-guarded          │
  │                             │ → a2a blocked              │
  │← cycle: phase=PR ──────────│                            │
  │── dispatch (final review) ────────────────────────────→│
  │                             │                            │ (汇总所有 verdict)
  │← verdict: all pass ───────────────────────────────────│
  │                             │                            │
  │ pr-merge-guarded ──────────│                            │
  │   develop <branch>          │                            │
  │                             │                            │
  │ wt-close --raw-key <key> ──│                            │
  │   (clean up both wts)      │                            │
```

**关键变化**：
- Worker 在 fix|feature worktree 完成全部开发阶段
- Manager 在 develop worktree 执行 merge + close
- Reviewer 直接对 Worker 发指令
- pr-review-guarded 被 checkpoint reviewer 替代
- 每个阶段后 Worker 主动 a2a blocked，等待 Reviewer GO

## 深入预研（续2）：A2A SQLite 状态机 vs 提示词约定

### Q8: 提示词约定的可靠性问题

之前的设计依赖 Worker agent prompt 中注入约定：

> "每轮开始检查 a2a state..."、"阶段完成调用 a2a-exit --state blocked..."

**问题**：Agent 可能忽略。就像今天 Worker 可以跳过 RED 一样，明天 Worker 可以跳过 HALT。提示词约定不是强约束。

**正确方案**：不在提示词里约定——在 **Manager 控制 Worker session 生命周期** 里强制。

### 核心洞察：每个 workflow 阶段 = 一个离散的 ACP prompt

Worker agent 不是"启动后跑全流程"。Worker agent 是 **Manager 逐 phase 喂 prompt**：

```
Manager:  session/prompt → "Do B1 for raw-xxx"
Worker:   执行 B1 → 写 a2a state=input-required (phase=B1) → prompt 结束
          （Worker session 空闲，等下一个 prompt）

Manager:  cycle 检测到 blocked → dispatch Reviewer
Reviewer: fork → review B1 → a2a update state=working + prompt "GO: do B2"

Manager:  检测到 state=working + phase=B1 cleared → 发送下一个 prompt
          session/prompt → "B1 passed. Now do B2 for raw-xxx"
Worker:   执行 B2 → 写 a2a state=input-required (phase=B2) → prompt 结束
...
```

**Worker 不是"等待"——Worker 是"完成当前 prompt 后就没有新 prompt 了"**。

Manager 控制节奏：什么时候发下一个 prompt、发什么内容。Worker 的"HALT"不是主动行为——是没有下一个 prompt 的自然结果。

### 三个 Agent 的协作模式

每个 raw issue 绑定一组 Agent，编号一一对应：

```
raw-xxx → manager_01  (主管，一个项目一个)
       → worker_03   (开发工位 worker，编号 = agent-table 分配的 worker slot)
       → reviewer_03 (worker_03 的配对 reviewer，编号对应 worker)
       
raw-yyy → manager_01  (同一个主管)
       → worker_05   (另一个工位)
       → reviewer_05
```

**并发模型**：

```
manager_01 (develop wt，一直运行)
  │
  ├── worker_03 (fix|feature wt) ←── reviewer_03 (fork manager_01)
  │     raw-xxx
  │
  ├── worker_05 (fix|feature wt) ←── reviewer_05 (fork manager_01)
  │     raw-yyy
  │
  └── worker_07 (fix|feature wt) ←── reviewer_07 (fork manager_01)
        raw-zzz
```

每个 worker_NN 独立运行在自己的 worktree，有自己配对的 reviewer_NN。

```
Agent              状态机              等待模式           触发方式
──────             ──────              ────────           ────────
manager_01         持续运行            永不等待            timer/cycle 自触发
                   submitted →         polling 循环       每 N 秒扫 a2a_tasks
                   cycling →                               
                   wt-close

worker_NN          逐 phase 运行       完成当前 prompt     manager_01 发 session/prompt
                   working →           后空闲              reviewer_NN 发 session/prompt  
                   blocked →
                   working → ...
                   completed

reviewer_NN        按需触发            完成当前 review     manager_01 dispatch
                   idle →              后空闲             a2a_tasks 新 blocked 事件
                   reviewing →
                   idle
```

**manager_01 永不阻塞**：
- manager_01 是 daemon 式循环：`while true; do freely cycle --all; sleep 30; done`
- 发现 blocked on worker_03 → dispatch reviewer_03 → 继续下一轮 cycle
- 发现 completed on worker_05 → wt-close --raw-key raw-yyy → 继续下一轮 cycle
- manager_01 不等 reviewer_NN 结果——下轮 cycle 自然会看到

**worker_NN ↔ reviewer_NN 是等待对**：
- worker_03: prompt 执行 → a2a blocked → prompt 结束 → 空闲
- reviewer_03: manager_01 dispatch → review → a2a working + prompt GO → 空闲
- worker_03: 收到 GO prompt → 执行下一 phase → a2a blocked → 空闲
- 循环直到 completed

### A2A SQLite 作为唯一的协调原语

不再依赖提示词约定。所有协调通过 `a2a_tasks` 表：

```
a2a_tasks 行状态流转:
                    Manager
                      │
                      │ INSERT (state=submitted)
                      ▼
  ┌──────────────────────────────────────┐
  │  state=submitted                     │
  │  Manager 创建 task，分配 worker       │
  └──────────────┬───────────────────────┘
                 │ Manager/ACP 启动 worker session
                 ▼
  ┌──────────────────────────────────────┐
  │  state=working                       │
  │  Worker 执行当前 phase               │
  │  message = "phase: B1"               │
  └──────────────┬───────────────────────┘
                 │ Worker 完成 B1 → PATCH /tasks/{id}
                 │ {state: "blocked", message: "phase: B1 done"}
                 ▼
  ┌──────────────────────────────────────┐
  │  state=input-required                       │
  │  Manager cycle 检测到                │
  │  → dispatch reviewer                 │
  │  Reviewer 评审...                    │
  └──────────────┬───────────────────────┘
                 │ Reviewer 完成 → PATCH
                 │ {state: "working", message: "GO: B2"}
                 │ + session/prompt to Worker
                 ▼
  ┌──────────────────────────────────────┐
  │  state=working                       │
  │  Worker 执行 B2                      │
  └──────────────┬───────────────────────┘
                 │ ...循环...
                 ▼
  ┌──────────────────────────────────────┐
  │  state=completed                     │
  │  Manager cycle 检测到                │
  │  → wt-close --raw-key <key>          │
  └──────────────────────────────────────┘
```

**关键**：只有两种角色可以改 state：
- Worker: working → blocked（完成 phase）
- Reviewer: blocked → working（GO/FIX）
- Manager: submitted → ... → completed（最终，或 force-close）
- Manager 也可以：任意 state → completed（--force）

### wt-close 的 reason 映射

| reason | 含义 | state |
|--------|------|-------|
| `达标完成` | 全 phase reviewer pass，正常 merge | completed |
| `不要了，丢弃` | 方案被否决，未 merge 提交丢弃 | completed + force_closed |
| `不做这个raw issue` | 从未开工位，只关平台 | completed + platform_only |
| `本地工位已删除` | wt-close --force 清理残留 | completed + force |

manager_01 在 wt-close 时把 reason 写入 a2a_tasks message 和 raw issue frontmatter。

### 修正后的 Phase 1 实现清单

1. **a2a_tasks 状态机**：完善 state 流转（submitted→working→blocked→working↻→completed），增加 message 字段记录 phase

2. **Worker agent prompt 模板**：每个 prompt 只包含一个 phase 的指令。Worker 完成后写 a2a blocked。**不依赖 Worker 自律**——Manager 控制 prompt 的发送节奏。

3. **`freely cycle`**：读 a2a_tasks 表（不是读 transcript），检测 blocked 任务，按 phase 匹配 reviewer 规则

4. **Reviewer dispatch**：Manager cycle 检测到 blocked → 创建 reviewer task（fork session）→ reviewer 读 phase 产物 → a2a update working + prompt GO/FIX

5. **Manager loop**：定时 cycle → 有 blocked 派 reviewer → 有 completed 做 wt-close

## 全流程泳道图：三 Agent 协作 + A2A 消息

```
时间 ──────────────────────────────────────────────────────────────────────────→

manager_01 (develop wt)         A2A/SQLite                  worker_NN (fix|feature wt)  reviewer_NN (fork manager_01)
  │                              │                           │                          │
  │ wt-create raw-xxx ──────────→│                           │                          │
  │                              │                           │                          │
  │ INSERT a2a_tasks             │                           │                          │
  │ {state: submitted,           │                           │                          │
  │  role: worker,               │                           │                          │
  │  raw_key: raw-xxx}           │                           │                          │
  │                              │                           │                          │
  │ ACP session/new ────────────→│── session/fork ──────────→│                          │
  │                              │                           │ Worker session 启动      │
  │                              │                           │                          │
  │ ═══════════════ PHASE B1 ════════════════════════════    │                          │
  │                              │                           │                          │
  │ session/prompt ─────────────→│── prompt ────────────────→│                          │
  │ "Do B1: brainstorm +         │                           │                          │
  │  candidate for raw-xxx"      │                           │                          │
  │                              │                           │                          │
  │                              │                           │ 读 raw issue             │
  │                              │                           │ 写 brainstorms.md        │
  │                              │                           │ 写 candidates.md         │
  │                              │                           │ 更新 milestones.md       │
  │                              │                           │                          │
  │                              │← PATCH /tasks/{id} ──────│                          │
  │                              │  {state: blocked,         │                          │
  │                              │   message: "phase:B1      │                          │
  │                              │    done, artifacts:       │                          │
  │                              │    brainstorms.md,        │                          │
  │                              │    candidates.md"}        │                          │
  │                              │                           │ (prompt 结束，空闲)       │
  │                              │                           │                          │
  │← cycle poll ────────────────│                           │                          │
  │  发现: state=input-required         │                           │                          │
  │  phase=B1, worker=worker_03  │                           │                          │
  │                              │                           │                          │
  │ INSERT a2a_tasks ───────────→│                           │                          │
  │ {state: submitted,           │                           │                          │
  │  role: reviewer,             │                           │                          │
  │  raw_key: raw-xxx,           │                           │                          │
  │  reviewer_for: worker_03,    │                           │                          │
  │  review_phase: "B1"}         │                           │                          │
  │                              │                           │                          │
  │ ACP session/fork ───────────→│──────────────────────────────────────────────────→│
  │                              │                           │   Reviewer session 启动  │
  │                              │                           │   (fork manager, 缓存命中)│
  │                              │                           │                          │
  │                              │                           │  读 B1 artifacts:        │
  │                              │                           │   brainstorms.md         │
  │                              │                           │   candidates.md          │
  │                              │                           │                          │
  │                              │                           │  判定: pass / fail       │
  │                              │                           │                          │
  │ ═══════════ REVIEWER VERDICT ═══════════════════════    │                          │
  │                              │                           │                          │
  │                 ┌─ IF PASS ────────────────────────────│──────────────────────────│
  │                 │                                       │                          │
  │                 │         │← PATCH /tasks/{id} ────────│← PATCH /tasks/{id} ─────│
  │                 │         │  {state: working}           │  (worker task)           │
  │                 │         │                             │                          │
  │                 │         │← session/prompt ───────────│← session/prompt ────────│
  │                 │         │  "GO: B1 passed.            │  "GO: B1 passed.         │
  │                 │         │   Now do B2: pre-tests,     │   Now do B2: pre-tests,  │
  │                 │         │   tasks, code-review"       │   tasks, code-review"    │
  │                 │         │                             │                          │
  │                 │         │                             │→ Worker 收到 prompt      │
  │                 │         │                             │→ 继续 B2                 │
  │                 │         │                             │                          │
  │                 ├─ IF FAIL ────────────────────────────│──────────────────────────│
  │                 │                                       │                          │
  │                 │         │← PATCH /tasks/{id} ────────│← PATCH /tasks/{id} ─────│
  │                 │         │  {state: working}           │  (worker task)           │
  │                 │         │                             │                          │
  │                 │         │← session/prompt ───────────│← session/prompt ────────│
  │                 │         │  "FIX: candidates.md        │  "FIX: candidates.md     │
  │                 │         │   missing acceptance_       │   missing acceptance_    │
  │                 │         │   criteria. Redo B1."       │   criteria. Redo B1."    │
  │                 │         │                             │                          │
  │                 │         │                             │→ Worker 收到 FIX         │
  │                 │         │                             │→ 重新做 B1               │
  │                 │         │                             │→ 再写 blocked            │
  │                 │         │                             │                          │
  │                 └─ verdict ────────────────────────────│──────────────────────────│
  │                              │                           │                          │
  │← cycle poll ────────────────│                           │                          │
  │  发现: state=working         │                           │                          │
  │  reviewer verdict: pass/fail │                           │                          │
  │  → 记录到 manager state      │                           │                          │
  │  → 如果 pass: 等下一轮 blocked│                           │                          │
  │  → 如果 fail: 等 worker 重做  │                           │                          │
  │                              │                           │                          │
  │ ═══════════ PHASE B2 (同上模式) ════════════════════    │                          │
  │  Manager → prompt → Worker   │                           │ B2 → blocked             │
  │  → cycle → dispatch reviewer │                           │                          │
  │  → Reviewer GO/FIX           │                           │                          │
  │                              │                           │                          │
  │ ═══════════ PHASE RED (同上模式) ════════════════════    │                          │
  │  Worker: RED → blocked       │                           │                          │
  │  Reviewer 重点查:             │                           │                          │
  │    actual_RED_output 是否     │                           │                          │
  │    占位符? evidence 真实?     │                           │                          │
  │                              │                           │                          │
  │ ═══════════ PHASE dev (同上模式) ════════════════════    │                          │
  │  Reviewer 重点查:             │                           │                          │
  │    实现是否匹配 B2 设计?       │                           │                          │
  │                              │                           │                          │
  │ ═══════════ PHASE GREEN (同上模式) ══════════════════    │                          │
  │  Reviewer 重点查:             │                           │                          │
  │    evidence_file 是否真实?    │                           │                          │
  │    逐条 actual_output vs      │                           │                          │
  │    expected_output ?         │                           │                          │
  │                              │                           │                          │
  │ ═══════════ PHASE PR ═══════════════════════════════    │                          │
  │                              │                           │                          │
  │ session/prompt ─────────────→│── prompt ────────────────→│                          │
  │ "GREEN passed. Run            │                           │                          │
  │  pr-create-guarded"           │                           │                          │
  │                              │                           │                          │
  │                              │                           │ pr-create-guarded        │
  │                              │                           │ → blocked                │
  │                              │                           │                          │
  │← cycle poll ────────────────│                           │                          │
  │  发现: state=input-required,         │                           │                          │
  │  phase=PR                     │                           │                          │
  │                              │                           │                          │
  │ INSERT a2a_tasks ───────────→│                           │                          │
  │ {review_phase: "PR"}         │                           │                          │
  │                              │                           │                          │
  │ ACP session/fork ───────────→│──────────────────────────────────────────────────→│
  │                              │                           │  最终评审                │
  │                              │                           │  汇总所有 phase verdict   │
  │                              │                           │                          │
  │                              │                           │  判定:                   │
  │                              │                           │  - all pass → 放行 merge │
  │                              │                           │  - 有 fail → GO/FIX      │
  │                              │                           │                          │
  │ ═══════════ FINAL VERDICT ══════════════════════════    │                          │
  │                              │                           │                          │
  │← cycle poll ────────────────│                           │                          │
  │  发现: state=input-required,         │                           │                          │
  │  final_verdict: pass          │                           │                          │
  │                              │                           │                          │
  │ ═══════════ MANAGER: MERGE + CLOSE ═════════════════    │                          │
  │                              │                           │                          │
  │ pr-merge-guarded ────────────│                           │                          │
  │   develop <branch>           │                           │                          │
  │                              │                           │                          │
  │ wt-close --raw-key <key> ────│                           │                          │
  │   → 删远程分支               │                           │                          │
  │   → 删 fix + test 工位       │                           │                          │
  │   → 关平台 issue              │                           │                          │
  │   → 删本地分支               │                           │                          │
  │                              │                           │                          │
  │ PATCH /tasks/{id} ──────────→│                           │                          │
  │  {state: completed,           │                           │                          │
  │   message: "达标完成"}        │                           │                          │
  │                              │                           │                          │
  │ ═══════════ DONE ═══════════════════════════════════    │                          │
```

### A2A 消息速查表

| # | 发送方 | A2A 动作 | 接收方 | 触发条件 | 接收方行为 |
|---|--------|---------|--------|---------|-----------|
| 1 | Manager | `INSERT state=submitted role=worker` | Worker | wt-create 后 | Worker session 启动，等第一个 prompt |
| 2 | Manager | `session/prompt "<phase>指令"` | Worker | phase 开始 | Worker 执行该 phase |
| 3 | Worker | `PATCH state=input-required message="phase:X done"` | Manager | phase 完成 | —（Worker prompt 结束，空闲） |
| 4 | Manager | cycle poll 检测到 blocked | — | 定时轮询 | Manager 读 message 取 phase，决定派 reviewer |
| 5 | Manager | `INSERT state=submitted role=reviewer` | Reviewer | 检测到 blocked + 新 phase | Reviewer session fork 启动 |
| 6 | Reviewer | `PATCH state=working` (worker task) | Worker | review 完成（GO/FIX） | Worker 收到新 state |
| 7 | Reviewer | `session/prompt "GO: <next>"` 或 `"FIX: <detail>"` | Worker | 同 #6 | Worker 收到 prompt，继续或返工 |
| 8 | Reviewer | `PATCH state=completed` (reviewer task) | Manager | review 结束 | Manager 下轮 cycle 读到 verdict |
| 9 | Manager | cycle poll 检测到 blocked + final_verdict=pass | — | 所有 phase pass | Manager 执行 pr-merge + wt-close |
| 10 | Manager | `PATCH state=completed` (worker task) | — | wt-close 后 | 记录最终状态和 reason |

### 关键设计决策

1. **Manager 不发 GO/FIX**。Reviewer 直接 PATCH worker task + session/prompt。Manager 只读 reviewer 的 verdict 结果。

2. **Worker 不轮询**。Worker 完成当前 phase 的 prompt 后自然空闲。下一个 prompt（来自 Reviewer 或 Manager）到达时自动继续。没有"检查状态"的约定——下一个 prompt 本身就是信号。

3. **Reviewer fork manager session**。缓存命中，冷启动成本低。独立上下文，不会被 worker 的"我做了"自述影响判断。

4. **Manager 是纯控制面**。不参与业务判断（"RED 过没过"），只做流程编排（"该派 reviewer 了"、"该 merge 了"、"该 close 了"）。

5. **所有状态变迁通过 A2A SQLite**。不依赖 agent 自律、不依赖提示词约定。Manager 轮询 SQLite 获取客观状态。

## 深入预研（续3）：卡点技术 —— 怎么稳定地让 Worker 停在 phase 边界

### Q9: 卡点的底层机制

"卡点"的本质：**Worker 在 phase 完成后不能再继续，必须等外部信号。**

四种技术方案：

| 方案 | 机制 | 可靠性 | 实现复杂度 |
|------|------|--------|-----------|
| A: Prompt 级门控 | Manager 不发下一个 prompt，Worker 自然空闲 | ★★★★★ ACP 协议保证 | 低 |
| B: Tool-call 门控 | Worker 调 `freely-checkpoint` tool，tool 内部轮询 a2a 等 GO | ★★★☆☆ tool 可能不被调用 | 中 |
| C: 进程级门控 | Worker session close，Manager restart | ★★★★☆ session 状态丢失 | 高 |
| D: stopReason 门控 | Worker 返回特定 stopReason，ACP bridge 拦截 | ★★★☆☆ ACP bridge 需改造 | 高 |

**决策：方案 A — Prompt 级门控。**

### 为什么 Prompt 级门控可靠

ACP `session/prompt` 模式的工作方式：

```
session/prompt → AI 处理 prompt → AI 返回 response → session 空闲等下一个 prompt
                                                              ↑
                                                         AI 不能自己继续
```

**关键**：ACP `session/prompt` 不是 `session/start`（自主模式）。AI 处理完当前 prompt 后**必须等下一个 prompt**。它不能"自己决定继续"。

这意味着：

```
Manager: session/prompt → "Do B1 for raw-xxx"
Worker:  读 raw issue → 写 brainstorms → 写 candidates → 
         PATCH a2a state=input-required → 返回 "B1 done"
         
         ↓ Worker 此刻的状态：session 空闲，等待下一个 prompt
         ↓ Worker 不能自己开始 B2 —— 没有 prompt 输入
         
Manager: cycle 检测到 blocked → dispatch reviewer
Reviewer: session/prompt → "GO: B2" 或 "FIX: redo B1"
         
         ↓ Worker 收到新 prompt → 执行
```

**卡点不是 Worker "主动停下"——是 Manager "不发车"。**

### 异常场景与稳定性

| 异常 | 表现 | 检测方式 | 恢复方式 |
|------|------|---------|---------|
| Worker 在 phase 中途崩溃 | ACP session 断开，a2a state 停在 working | Manager cycle: session/ping 超时 + state=working 超过 N 分钟 | `PATCH state=input-required message="worker crashed"` → 重新启动 Worker session → session/prompt "resume from last checkpoint" |
| Worker 完成 phase 但忘记写 blocked | Worker 返回了 response 但没有 PATCH a2a | Manager cycle: session 空闲 + state=working | Manager 自己 PATCH blocked（读 Worker response 判断 phase） |
| Reviewer 崩溃 | reviewer task state=working 超时 | Manager cycle: reviewer task 创建超过 N 分钟未 completed | Manager PATCH reviewer task state=failed → 重新 dispatch |
| Worker 收到 FIX 但不改 | Worker 重做 phase 但 same issues | Reviewer 下轮 cycle 再次 fail，相同 reason | 连续 2 次 same fail → escalate 到 Manager → Manager 决定 force-close 或换 worker |
| Worker 执行超时 | phase 超过 N 分钟未 blocked | Manager cycle: state=working + elapsed > timeout | session/cancel? → 其实没有 cancel。改用：Manager 发新 session/prompt 注入 "__FREELY_CHECKPOINT__ 请停止当前工作并汇报进度" |
| A2A Server 宕机 | PATCH 失败 | a2a_task.py 返回 error | 重试 + backoff。超过 N 次 → Manager 告警 |
| SQLite 锁冲突 | 并发 PATCH 冲突 | SQLite BUSY | WAL 模式下自动 retry。busy_timeout=5000ms |

### Worker 忘记写 blocked 的最后防线

虽然 Prompt 级门控下 Worker "不能继续"，但 Worker 可能在返回 response 前忘记 PATCH a2a。此时 a2a state 仍为 working。

**双重保险**：

```
T1: 正常路径
  Worker 返回 response + PATCH state=input-required
  → Manager cycle 检测到 blocked ✓

T2: Worker 忘记 PATCH
  Worker 返回 response，但 state 仍是 working
  → Manager cycle: session 空闲（无 in-flight prompt）+ state=working
  → Manager 读 Worker response 文本，解析 phase 标记
  → Manager 自己 PATCH state=input-required
  → 继续正常流程

T3: Worker response 中也无法解析 phase
  → Manager PATCH state=input-required message="unknown phase, manual inspection needed"
  → escalate 到人工
```

**Manager cycle 的检测逻辑**：

```python
def cycle(raw_key):
    task = a2a.get_task(raw_key)
    
    if task.state == "blocked":
        phase = parse_phase(task.message)  # "phase: B1 done"
        if phase and not already_reviewed(phase):
            dispatch_reviewer(raw_key, phase)
    
    elif task.state == "working":
        elapsed = now - task.updated_at
        session_alive = acp.ping(task.session_id)
        
        if not session_alive and elapsed > TIMEOUT:
            # Worker crashed
            patch(task, state="blocked", message="worker session lost")
        elif not session_alive and elapsed < TIMEOUT:
            # Worker finished prompt but forgot to write blocked
            response = acp.get_last_response(task.session_id)
            phase = parse_phase(response)
            if phase:
                patch(task, state="blocked", message=f"phase: {phase} done")
            else:
                # Can't determine phase — need manual inspection
                patch(task, state="blocked", message="unknown phase, inspect")
    
    elif task.state == "completed":
        wt_close(raw_key, reason="达标完成")
```

### Q10: 怎么准确判断当前是哪个 phase —— 文件系统产物检测

**不信任 Worker 自报**。Worker 写 `"phase: B1 done"` 可能写错、写漏、写假。Manager 直接读 fix|feature worktree 文件系统，按 phase 顺序检查。

**每个 phase 的检测规则**（按 workflow 顺序，后面的 phase 意味着前面的已完成）：

```
Phase    必须存在                              必须不存在（下一 phase 未开始）
──────   ──────────────────────────────────    ──────────────────────────────────
B1       candidates.md + brainstorms.md        docs/epics/*/ 下无此 raw key 目录
         且 candidate.status=promoted           (B2 尚未物化)

B2       pre-tests.md + tasks.md               pre-tests 全部 pending
         且 I-* issue phase_state=done_b2_ibm  (RED 尚未执行)

RED      pre-tests 全部 item                   全部 item red-green-status != green
         red-green-status=red                  (GREEN 尚未通过)
         且 actual_RED_output 非空

dev      git diff base..HEAD 有变更            全部 item red-green-status != green
         且 implementation decision note 存在   (GREEN 尚未通过)

GREEN    pre-tests 全部 item                   全部 item actual_output 已填
         red-green-status=green                pr-create-gate-passed 不存在
         且 evidence_file 存在且 >1 行          (PR 尚未创建)

PR       pr-create-gate-passed 存在            wt-close 未执行
         且 GitHub PR number 可知               (工位仍存在)
```

**为什么这是准确的**：

1. **文件系统是客观证据**。Worker 可以撒谎说"RED done"，但 `red-green-status=red` 是在 pre-tests.md 文件里的——Manager 直接读文件。Worker 改没改文件，一看便知。

2. **顺序强制**。不只看当前 phase 的产物存在，还看下一个 phase 的产物**不存在**。防止 Worker 跳 phase（比如跳过 B2 直接写代码）。

3. **文件内容验证**。不只是文件存在——还检查内容。`evidence_file` 必须 >1 行（防 ghost pass）。`actual_RED_output` 必须非空。

**Manager cycle 的 phase 检测伪代码**：

```python
def detect_phase(worktree_path, raw_key):
    wt = worktree_path
    
    # Check in reverse order (most advanced first)
    if exists(f"{wt}/.freely/run/pr-create-gate-passed"):
        return "PR"
    
    pre_tests = find_pre_tests(wt, raw_key)
    if pre_tests:
        items = parse_acceptance_items(pre_tests)
        all_green = all(i.red_green_status == "green" for i in items)
        all_evidence_real = all(file_lines(i.evidence_file) > 1 for i in items)
        if all_green and all_evidence_real:
            return "GREEN"
        all_red = all(i.red_green_status == "red" for i in items)
        if all_red:
            return "RED"
        return "B2"  # pre-tests exist but not all red/green = still in B2
    
    candidates = find_candidates(wt, raw_key)
    if candidates and candidates.status == "promoted":
        return "B1"
    
    if git_diff_has_code_changes(wt):
        return "dev"  # code exists but no pre-tests → skipped B2 (shouldn't happen)
    
    return "unknown"
```

**与 Worker 自报的关系**：

Worker 仍然写 `a2a state=input-required`——但 message 字段是**辅助信息**，不是判定依据。Manager 用文件系统检测确认 phase 后才 dispatch reviewer。

```
Worker: PATCH state=input-required message="phase:B1 done"
Manager: cycle → 读文件系统 → 确认 candidates.md 存在且 promoted → 
         确认这是 B1 → dispatch reviewer(phase="B1")
```

如果 Worker 自报与文件系统不符（比如 Worker 说 "RED done" 但 pre-tests 还是 pending），Manager 以文件系统为准，标记异常。

### 超时与异常配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `PHASE_TIMEOUT` | 30 min | 单个 phase 最大执行时间 |
| `REVIEW_TIMEOUT` | 10 min | Reviewer 单次 review 最大时间 |
| `CYCLE_INTERVAL` | 30 sec | Manager cycle 轮询间隔 |
| `SESSION_PING_TIMEOUT` | 5 sec | ACP session/ping 超时 |
| `MAX_CONSECUTIVE_FAILS` | 2 | 同一 phase 连续 fail 次数上限 |

### Q11: 文件检测不可靠——phase 判断是语义问题，应由 Reviewer 解决

**文件检测的致命缺陷**：

| 场景 | 文件检测结果 | 实际情况 |
|------|------------|---------|
| Worker 跳过 RED 直接写 GREEN | `red-green-status=green` 全部 green → 判定 GREEN 完成 | RED 从未执行，`actual_RED_output` 全是占位符 |
| Worker 用 `FREELY_SKIP_IBM_GATE` 跳过 B1/B2 | 没有 brainstorms/candidates/pre-tests | Worker 直接 feedback → wt-create → wt-close，合法但流程不完整 |
| Worker 多个 phase 不 commit | git log 只有一个 commit | 无法从 commit 历史判断 phase 顺序 |
| Worker 伪造文件内容 | `evidence_file` 存在且 >1 行 | 内容是 "GREEN: PASS" 一行重复 3 遍 |

**根本原因**：phase 完成质量是**语义判断**，不是文件存在性判断。脚本能检测"文件是否存在"，但检测不了"RED 是否真的执行了"。

**正确方案**：文件系统只是触发信号。真正的 phase 检测由 Reviewer 做。

```
Manager cycle 的职责（缩小）：
  1. 检测 a2a state=input-required（Worker 声称完成了什么）
  2. 读出 Worker 写的 message（"phase: B1 done"）
  3. 派 Reviewer："请验证 worker 声称 B1 完成，检查所有前置步骤是否按顺序完成"
  4. 收 verdict，记录状态

Reviewer 的职责（扩大）：
  1. 收到 review 任务（phase=X）
  2. 检查所有前置 phase 是否真实完成且按顺序：
     - B1 完成？→ 读 candidates.md，判断方案是否充分
     - B2 完成？→ 读 pre-tests.md，判断测试设计是否真实
     - RED 完成？→ 读 actual_RED_output，判断是否占位符
     - dev 完成？→ 读 git diff，判断实现是否匹配 B2 设计
     - GREEN 完成？→ 读 evidence_file，判断是否 ghost pass
  3. 检查当前 phase 的产出质量
  4. 返回 verdict + 修复建议
```

**顺序验证**：

Reviewer 从 git log 获取提交顺序。如果 Worker 每个 phase 都有 commit，顺序清晰。如果 Worker 多个 phase 合在一个 commit，Reviewer 从内容推断：

```
例: 一个 commit 包含 pre-tests.md (全部 green) + 代码变更 + evidence 文件
Reviewer 判断: 
  - pre-tests.md 里有 RED→GREEN 的流转吗？没有 actual_RED_output → RED 被跳过
  - evidence 文件是真实输出还是占位符？一行 "PASS" → ghost pass
  → verdict: fail, "RED 未执行, GREEN evidence 不可信"
```

**`FREELY_SKIP_IBM_GATE` 的卡点行为**：

```
正常 fix|feature 流程:
  feedback → wt-create → B1 → B2 → RED → dev → GREEN → pr-create → pr-merge → wt-close
  每个 → 都是卡点

IBM skip 流程:
  feedback → wt-create → wt-close
  Manager cycle 检测: state=input-required, phase 无法识别
  → 没有 brainstorms, 没有 pre-tests, 没有 evidence
  → Reviewer 判断: "IBM 治理链路缺失，检查是否 FREELY_SKIP_IBM_GATE"
  → 如果是合法 skip（纯文档/清理/格式化）→ pass
  → 如果不应 skip → fail
```

**Manager 不再做 phase 检测**。Manager 只做：

```
1. 检测 a2a state=input-required → 触发 review
2. 收 verdict → 记录
3. 超时检测 → 告警
4. 最终 completed → wt-close
```

**Reviewer 做所有的语义判断**：是否按顺序、是否真实执行、是否质量达标。

## 行业对标：A2A 协议标准 + AI CLI 内部多 Agent 协作

### Google A2A 协议标准（2025.04）

Google A2A 是 Linux Foundation 托管的开放标准，定义 Agent 间协作原语：

```
Task 状态机（标准）:
  submitted → working → input-required → completed
                       ↘ failed
                       ↘ canceled

Freely a2a_tasks 映射:
  submitted → working → blocked → completed
                       ↘ failed
```

**Freely 的 `blocked` 就是 A2A 标准的 `input-required`**——语义一致：Agent 完成当前工作，等待外部输入（reviewer 的 GO/FIX）。

**标准协作模式**（从开源实现中提取）：

| 模式 | 开源实现 | Freely 对应 |
|------|---------|------------|
| Coordinator/Sub-agent | tRPC-A2A-Go | manager_01 派 worker_NN + reviewer_NN |
| Facilitator/Worker | @lucid-agents | reviewer_NN 对 worker_NN 发 GO/FIX |
| Handoff/Transfer | Teams SDK, transfer events | a2a_tasks state 变迁 = 交接信号 |
| Multi-round structured | OpenSpawn (4-round ideation) | B1→B2→RED→dev→GREEN→PR 每个 phase 一轮 |
| Router/Registry | distributed-a2a | agent-table.toml = registry, manager_01 = router |

**结论**：Freely 的设计符合 A2A 标准。`blocked` 是标准 `input-required` 的 checkpoint gate 扩展。整个 phase 卡点 → a2a_tasks 写 → reviewer 消费 → GO/FIX 的流程就是标准的 A2A 多 Agent 协调。

### Claude Code 内部子 Agent 架构

Claude Code 的子 Agent（Task tool / I2A）提供对照：

```
Claude Code:
  Main Agent ──(task description)──▶ Subagent（context 隔离）
                                    │ 独立 session, 独立 tool 权限
  Main Agent ◀──(final report)──── Subagent
  ⚠️ 执行期间无双向通信
  ⚠️ 无持久 Agent（完成后销毁）
  ⚠️ 无内置 handoff
  ⚠️ Flat 架构（子 Agent 不能再派子 Agent）
```

**Claude Code 缺的，正是 Freely 要做的**：
- CC 子 Agent 无过程监督 → Freely manager_01 cycle 轮询
- CC 无阶段卡点 → Freely phase checkpoint + reviewer_NN
- CC 无持久 Agent → Freely worker_NN 跨 phase 保持 session
- CC 无交接协议 → Freely a2a_tasks state 机

### 行业最佳实践总结：Agent 到特定位置写特定格式的交接信息

**不是"依赖 Agent 自律"——是"协议层保证"**：

1. **Google A2A**：`tasks/send` → Server 必须按 state 机返回。Agent 写错 state？Server 拒绝非法 state 转换。

2. **tRPC-A2A-Go**：Coordinator 不信任 Sub-agent 的 text response。读 `Task.status` 和 `Task.artifacts`——结构化字段，不是自然语言。

3. **Teams SDK Handoff**：handoff payload 是结构化 JSON（`kind: "handoff"`, `from`, `summary`），不是 Agent 自由文本。

4. **Claude Code Subagent**：Main agent 不读 subagent 的对话历史。只读 `Task tool result`——结构化返回。

**Freely 的对应设计**：

```
不信任: Worker 说 "B1 done" → 信任: a2a_tasks.state = "blocked" + message = "phase: B1"
不信任: Worker 自述 "RED passed" → 信任: pre-tests.md 中 red-green-status 字段值
不信任: Worker 说 "evidence 真实" → 信任: evidence_file 文件内容行数 + reviewer_NN 语义审核
```

**交接信息格式（a2a_tasks.message）**：

```json
{
  "phase": "B1",
  "status": "done",
  "artifacts": [
    "docs/pre-brainstorms/20260630T002621Z--supervisor-cycle-monitor/brainstorms.md",
    "docs/pre-brainstorms/20260630T002621Z--supervisor-cycle-monitor/candidates.md"
  ],
  "next_phase": "B2",
  "timestamp": "2026-06-30T01:00:00Z"
}
```

结构化、可机读、可验证。不是自然语言 "I think I'm done with B1"。

### Q12: 用标准 `input-required` 而非自定义 `blocked`，补上 `canceled`

**为什么用 `input-required`**：

Google A2A 标准中 `input-required` 的定义：

> The agent needs more information from the client before it can continue processing the task.

Freely 的每个 workflow phase 边界正好是这个语义：
- worker_NN 完成 B1 → **需要 reviewer_NN 的 GO/FIX 才能继续 B2**
- worker_NN 完成 RED → **需要 reviewer_NN 的审核结果才能继续 dev**
- ...

`input-required` 完美描述了这个状态。不需要发明 `blocked`。

**补上 `canceled`**：

A2A 标准有三个终止态：`completed`、`failed`、`canceled`。Freely 缺 `canceled`。

| 终止态 | 含义 | Freely 触发条件 |
|--------|------|----------------|
| `completed` | 正常完成 | 全部 phase reviewer pass → merge → wt-close |
| `failed` | Agent 崩溃/出错 | worker_NN session 断开且无法恢复 |
| `canceled` | 主动取消 | manager_01 --force 丢弃 / 方案被否决 / 不再需要 |

**完整状态机**：

```
                    manager_01 INSERT
                         │
                         ▼
  ┌──────────┐     ┌──────────┐     ┌────────────────┐     ┌───────────┐
  │ submitted │────▶│ working  │────▶│ input-required │────▶│ completed │
  └──────────┘     └────┬─────┘     └───────┬────────┘     └───────────┘
                        │                   │
                        │ worker_NN 崩溃     │ reviewer_NN GO/FIX
                        ▼                   │ (PATCH state=working
  ┌──────────┐     ┌──────────┐              │  + prompt "GO: next phase")
  │  failed  │     │ canceled │◀─────────────┘
  └──────────┘     └──────────┘ manager_01 主动取消
```

**每个 phase 边界触发 `input-required` 的机制**：

不是"Worker 自觉写"——是 **Worker prompt 的结尾指令**：

```
Manager 发 prompt:
  "Do B1 for raw-xxx. When done:
   1. Write brainstorms.md and candidates.md
   2. PATCH a2a state=input-required, message='{\"phase\":\"B1\",\"status\":\"done\"}'
   3. Stop. Do NOT continue to B2."

Worker 执行:
  → 写文件
  → PATCH /tasks/{id} {state: "input-required", message: {...}}
  → 返回 "B1 done"
  → prompt 结束，session 空闲

manager_01 cycle:
  → 检测到 state=input-required + phase=B1
  → INSERT reviewer task
  → reviewer_NN fork → review → PATCH worker state=working + prompt "GO: B2"
```

**Worker 不能跳过 `input-required`**——prompt 指令明确说 "Stop. Do NOT continue." 而且 prompt 结束后 session 空闲，没有下一个 prompt 就不可能继续。双重保证：指令 + 协议。

### 修正后的 a2a_tasks.message 格式

```json
// Worker 完成 phase 时写入:
{
  "phase": "B1",
  "status": "done",
  "artifacts": [
    "docs/pre-brainstorms/{key}--{slug}/brainstorms.md",
    "docs/pre-brainstorms/{key}--{slug}/candidates.md"
  ],
  "timestamp": "2026-06-30T01:00:00Z"
}

// Reviewer 审核后写入 (GO):
{
  "phase": "B1",
  "verdict": "pass",
  "reviewer": "reviewer_03",
  "next_phase": "B2",
  "timestamp": "2026-06-30T01:05:00Z"
}

// Reviewer 审核后写入 (FIX):
{
  "phase": "B1",
  "verdict": "fail",
  "reviewer": "reviewer_03",
  "reason": "candidates.md missing acceptance_criteria",
  "action": "redo B1 with complete acceptance_criteria",
  "timestamp": "2026-06-30T01:05:00Z"
}
```

### Q13: `input-required` 不等于 "送 reviewer"——需要 reason 区分

`input-required` 是 A2A 标准状态，语义是 "Agent 需要外部输入才能继续"。但"外部输入"不只有 reviewer 一种来源：

```
input-required 的 reason 分类:

1. phase_completed      worker_NN 完成 B1/B2/RED/dev/GREEN/PR → 需要 reviewer_NN 审核
                        触发: manager_01 dispatch reviewer_NN
                        
2. need_clarification   worker_NN 遇到模糊的 raw issue 描述 → 需要 manager_01 澄清
                        触发: manager_01 介入，回答后 state→working
                        
3. blocked_by_env       worker_NN 遇到环境问题（网络不通、依赖缺失）→ 需要 manager_01 修复
                        触发: manager_01 处理环境，修复后 state→working

4. wt_close             manager_01 主动关闭 → state→completed
                        这是唯一进入 completed 的路径
```

**`completed` 只有 manager_01 能设**：

Worker 不能自己判定 "我做完了"。Worker 在每个 phase 完成时设 `input-required`（reason=phase_completed）。全部 phase 通过 reviewer 审核后，manager_01 执行 pr-merge + wt-close，才设 `state=completed`。

```
反例（不允许）:
  Worker: "B1 B2 RED dev GREEN 都做了，a2a-exit --state completed"
  → 不允许。Worker 不知道质量。只有 reviewer_NN 逐 phase 审核 + manager_01 merge 后才是真的完成。

正例:
  Worker: B1 done → a2a-exit --state input-required (reason: phase_completed, phase: B1)
  reviewer_NN: pass → a2a state=working + prompt "GO: B2"
  ... 全部 phase pass ...
  manager_01: pr-merge + wt-close → PATCH state=completed
```

**reviewer 的 verdict 从不设 `completed`**：

reviewer 的 GO/FIX 是让 Worker 继续下一 phase 或返工——不是终章。只有 wt-close 是终章。

### a2a_tasks.message 完整格式

```json
// Worker 设 input-required (phase completed, need review)
{
  "reason": "phase_completed",
  "phase": "B1",
  "artifacts": ["brainstorms.md", "candidates.md"],
  "timestamp": "2026-06-30T01:00:00Z"
}

// Worker 设 input-required (need clarification)
{
  "reason": "need_clarification",
  "question": "raw issue 描述中 '优化性能' 太模糊，请明确具体指标",
  "timestamp": "2026-06-30T01:10:00Z"
}

// reviewer 设 working + GO
{
  "verdict": "pass",
  "phase": "B1",
  "reviewer": "reviewer_03",
  "next": "B2",
  "timestamp": "2026-06-30T01:05:00Z"
}

// reviewer 设 working + FIX
{
  "verdict": "fail",
  "phase": "B1",
  "reviewer": "reviewer_03",
  "issues": ["candidates.md missing acceptance_criteria"],
  "action": "redo B1 with complete acceptance_criteria",
  "timestamp": "2026-06-30T01:05:00Z"
}

// manager_01 设 completed (wt-close)
{
  "reason": "wt_close",
  "close_reason": "达标完成",
  "timestamp": "2026-06-30T02:00:00Z"
}
```

### state 转换权限矩阵

| state 转换 | worker_NN | reviewer_NN | manager_01 |
|-----------|-----------|-------------|------------|
| working → input-required | ✅ (phase done / need help) | ❌ | ❌ |
| input-required → working | ❌ | ✅ (GO/FIX) | ✅ (clarification reply) |
| input-required → canceled | ❌ | ❌ | ✅ (主动放弃) |
| working → failed | ✅ (自身崩溃) | ❌ | ✅ (超时) |
| any → completed | ❌ | ❌ | ✅ (wt-close) |

### Q14: Task 分配与发现——A2A 标准 vs Freely 共享 DB 模型

**Google A2A 标准模型**：

```
Client → POST https://agent-A.example.com/tasks/send → Agent A 处理
```
Task 发给特定 Agent 的 endpoint。分配是**隐式**的——发给谁就是谁的。

Agent Card 字段（标准）：
```json
{
  "name": "Code Reviewer",
  "url": "https://reviewer.example.com",
  "capabilities": { "skills": ["code-review"] }
}
```

**Freely 的共享 DB 模型**：

所有 Agent 共用一个 SQLite `a2a_tasks` 表。没有 per-agent HTTP endpoint。分配必须**显式**——task 上标记 `agent_id`。

```
a2a_tasks 表字段:
  task_id     ← UUID，A2A 标准
  agent_id    ← Freely 扩展。谁负责这个 task（worker_03 / reviewer_03）
  raw_key     ← Freely 扩展。关联哪个 raw issue
  state       ← A2A 标准: submitted/working/input-required/completed/failed/canceled
  role        ← worker | reviewer | manager
  message     ← A2A 标准。交接信息 JSON
  context_id  ← A2A 标准。同一个 raw issue 的所有 task 共享一个 context_id
```

**Agent 如何发现"有我的活"**：

```
方式1: Polling（当前）
  worker_03: SELECT * FROM a2a_tasks WHERE agent_id='worker_03' AND state='working'
  reviewer_03: SELECT * FROM a2a_tasks WHERE role='reviewer' AND raw_key='raw-xxx' AND state='submitted'

方式2: SSE 推送（A2A 标准支持）
  GET /tasks/stream ← SSE 事件流
  worker_03 订阅: state 变更 → 推送 TaskStatusUpdateEvent
  reviewer_03 订阅: 新 submitted task → 推送
```

**围观者（谁需要知道 task 状态变化）**：

| Task 事件 | manager_01 | worker_NN | reviewer_NN |
|-----------|-----------|-----------|-------------|
| worker task created (submitted) | ✅ 创建者 | ✅ 我是 agent_id | ❌ |
| worker task → input-required | ✅ cycle 检测到 → dispatch | ✅ 我设的 | ✅ 需要我 review |
| reviewer task created | ✅ 创建者 | ❌ | ✅ agent_id 是我 |
| reviewer task → working | ✅ verdict 已给 | ✅ 收到 GO/FIX | ✅ 我设的 |
| any task → completed | ✅ wt-close | ❌ (已结束) | ❌ |

**"我该领取哪个 task"的判断逻辑**：

```
worker_03:
  1. 查 a2a_tasks WHERE agent_id='worker_03' AND state='working'
  2. 读 message 字段 → 知道当前 phase
  3. 执行 phase → 设 state=input-required

reviewer_03:
  1. 查 a2a_tasks WHERE role='reviewer' AND raw_key='raw-xxx' AND state='submitted'
  2. 读 message → 知道 review phase
  3. Fork session → review → 设 worker task state=working + prompt GO/FIX

manager_01:
  1. cycle 扫所有 raw_key: SELECT * WHERE state='input-required'
  2. 按 reason 分派: phase_completed→reviewer, need_clarification→自己回答
  3. 扫 state='completed' → wt-close
```

### Q15: a2a-state-standard #3639 与本 candidate 的关系

#3639（a2a state 标准化）是**前置依赖**——先把状态名对齐 A2A 标准，supervisor-cycle 才能用标准状态名。

| #3639 交付 | 本 candidate 依赖 |
|-----------|-----------------|
| `state=input-required` | cycle 检测 `input-required` 触发 dispatch |
| `state=canceled` | manager_01 主动取消 |
| `--state` 替代 `--kind` | Worker prompt 指令 `a2a-exit --state input-required` |
| `agent_id` 字段 | task 分配和领取 |
| SSE streaming | 实时推送（Phase 2） |

### Q16: Agent Card + ACP/A2A 集成——现有基础与缺口

**已有基础设施**：

```
agent-table.toml (Agent Card 的 Freely 实现):
  [[agents]]
  manager_id = "manager_01"     ← Agent Card name
  manager_slot = "claude-apikey-ds-pro-auto"  ← AI CLI tool+account
  
  [[agents]]
  worker_id = "worker_01"
  worker_slot = "claude-apikey-ds-pro-auto"
  reviewer_id = "reviewer_worker_01"  ← 配对 reviewer
  reviewer_slot = "claude-apikey-ds-pro-auto"
  pool = 10                           ← worker_01~worker_10 + reviewer_01~reviewer_10

agent-card-schema.md (A2A 标准 Agent Card 的 Freely 扩展):
  - A2A 标准字段: name, url, version, capabilities
  - Freely 扩展: worktreeIsolation, supportedExitKinds, skills, socketPath
```

**现有 ACP/A2A 流程**（acp-a2a-architecture.md）：

```
Manager → a2a-exit --state=submitted --role=worker → A2A Server
Runtime → tasks/list --state=submitted --role=worker → build prompt
Runtime → ACP session/fork → Worker session 启动
Worker → a2a-exit --state=input-required → A2A Server
Runtime → tasks/list → 检测到 input-required → ???
                                                  ↑
                                          目前缺：不知道该做什么
```

**缺口**：

| 能力 | 现有 | 需要 |
|------|------|------|
| Agent Card 定义 | agent-table.toml + schema | ✅ 够用，需加 `reviewer_for` 配对字段 |
| Runtime SSE 监听 | A2A Server 有 SSE /stream | Runtime 侧需加 SSE client |
| SSE → ACP 触发 | 无 | input-required → dispatch reviewer (session/fork) |
| reviewer → worker 通信 | 无 | reviewer verdict → ACP session/prompt to worker |

**补齐后的完整链路**：

```
Worker → a2a-exit --state=input-required (reason=phase_completed, phase=B1)
  → A2A Server → SSE event → Runtime
  → Runtime: state=input-required, reason=phase_completed
  → Runtime: SELECT reviewer_id FROM agent-table WHERE worker_id='worker_03'
  → Runtime: ACP session/fork → reviewer_03 session 启动
  → reviewer_03: review B1 artifacts → verdict
  → reviewer_03: a2a-exit --state=completed (reviewer task done)
  → reviewer_03: PATCH worker task state=working + message GO/FIX
  → A2A Server → SSE event → Runtime
  → Runtime: state=working on worker task
  → Runtime: ACP session/prompt → "GO: B2" (or "FIX: ...")
  → worker_03: 收到 prompt → 继续下一 phase
```

**Agent Card 在 agent 上下文中的使用**：

Agent 启动时，Runtime 从 `agent-table.toml` 读取：
```
worker_03 的身份定义:
  - 我是谁: worker_03
  - 我的 reviewer: reviewer_worker_03
  - 我的 AI tool: claude-apikey-ds-pro-auto
  - 我的 worktree: /path/to/fix-worktree
  - 我的 raw key: raw-xxx
```

这些信息通过 prompt 注入 Agent session 上下文——Agent 知道自己是谁、能调 `a2a-exit`、知道 reviewer 编号。

**与 `agent_id` 字段的关系**：

```
a2a_tasks 表:
  task_id = "task-001"
  agent_id = "worker_03"    ← 谁负责执行
  reviewer_id = "reviewer_worker_03"  ← 谁负责审核
  raw_key = "raw-xxx"
  state = "input-required"
```

`agent_id` 把 task 绑定到特定 Agent 实例。`reviewer_id` 配对从 agent-table 查询。多 worker 并发时靠编号区分。

### Q17: session/fork vs session/prompt 决策 + Agent Card 完整性

**session/fork vs session/prompt 决策逻辑**：

Agent 可能已有 session（之前启动过），需要判断：

```
Runtime 需要启动 reviewer_03:
  1. 查 agent-id.env: /path/to/worktree=reviewer=reviewer_03 → session_id=abc123
     有 session_id → session/prompt（复用已有 session）
     无 session_id → session/fork（fork manager session，新建）
  2. session/fork 后:
     - 获得新 session_id
     - 写回 agent-id.env: /path/to/worktree=reviewer=reviewer_03=session_id=xyz789
  3. 下次需要 reviewer_03 时:
     - agent-id.env 已有 session_id=xyz789
     - session/prompt（复用，缓存命中）
```

当前代码（freely line 4087-4093）处理了 fork 的 UUID 生成，但缺少：
- agent-id.env 查询逻辑
- "有 session → prompt，无 session → fork" 的决策分支
- session/prompt 后写回 agent-id.env

**Agent Card 完整性——对标 Zed ACP client**：

Zed 的 `agent_servers` 配置：
```json
{
  "agent_servers": {
    "claude-code": {
      "command": "npx",
      "args": ["claude-code-acp", "--skills", "./skills,~/.deepagents/skills"]
    }
  }
}
```

关键：`--skills` 是**文件系统路径**，不是 skill 名。因为不同 AI CLI tool 的文件系统布局不同。

Freely 的 `agent-table.toml` 当前：
```toml
[[agents]]
worker_id = "worker_01"
worker_slot = "claude-apikey-ds-pro-auto"   # ← 只有 slot 名
```

缺 A2A 标准字段：
```toml
# 需要补齐:
agent_name = "Freely Worker"          # A2A: name
agent_version = "1.0.0"              # A2A: version  
agent_url = "unix:///tmp/freely-a2a-{hash}.sock"  # A2A: url
capabilities = {streaming=true, pushNotifications=true}  # A2A: capabilities

# 多 tool 支持:
skills_path = "docs/system/workspace/skills/"   # 所有 tool 通用
# 或 per-tool:
[tool.cc]
skills_path = "docs/system/workspace/skills/"
[tool.codex]
skills_path = "docs/system/workspace/skills/"    # 不同 tool 可能有不同路径
```

**Zed vs Freely 对比**：

| 维度 | Zed (ACP client) | Freely (ACP client) |
|------|-----------------|-------------------|
| Agent 配置 | `settings.json` agent_servers | `agent-table.toml` |
| 多 tool 支持 | 每个 agent_server 各自 command+args | agent_slot 映射到 ~/.ai-auth/ |
| Skills 路径 | `--skills ./path` 完整路径 | 缺，只有 skill 名 |
| Agent Card | 内置在 ACP server | agent-card-schema.md (文档) + agent-table.toml (运行时) |
| Session 管理 | session/new, session/prompt | 同，但缺 agent-id.env 查询逻辑 |

**agent-table.toml 对标 Agent Card 需要补的**：

```toml
# 补 A2A 标准字段:
agent_name = "Freely Worker"          # A2A: name
agent_version = "1.0.0"              # A2A: version  
agent_url = "unix:///tmp/freely-a2a-{hash}.sock"  # A2A: url
capabilities = {streaming=true, pushNotifications=true}  # A2A: capabilities

# 补 supportedSkills（skill 名列表，不是路径）:
supportedSkills = [
  "freely-workflow-guarded-execution",
  "freely-doc-B1_IBM-execution",
  "freely-doc-B2_IBM-execution",
  "freely-test-RED-execution",
  "freely-dev-loop-execution",
  "freely-test-execution"
]

# 已有的保留:
worker_slot = "claude-apikey-ds-pro-auto"   # tool+account
reviewer_id = "reviewer_worker_01"           # 配对 reviewer
```

**不需要 `skills_path`**：`deploy-skills` 已经管了路径映射（`docs/system/workspace/skills/` → `~/.tool/skills/`）。Agent prompt 用 `skill:<name>` 引用，工具自己解析。多 tool 场景下每个 tool 的 ACP server 从自己的目录读。Agent Card 只需要声明**支持哪些 skill**，不需要声明路径。

**修复清单**：

1. `agent-table.toml` 补 A2A 标准字段（name, version, url, capabilities, supportedSkills）
2. Runtime 补 session/fork vs prompt 决策逻辑（查 agent-id.env）
3. agent-id.env 补 session_id 字段（当前只有 worktree→role→agent_id）

## B1 综合收敛

> 以下综合 Q1-Q17 全部讨论结果。前半段（Q1-Q7）中部分结论已被后半段（Q8-Q17）修正或推翻。本节是最终统一设计。

### 最终架构（已推翻的用 ~~删除线~~ 标记）

| 维度 | 早期结论 | 最终结论 | 推翻原因 |
|------|---------|---------|---------|
| 卡点机制 | ~~Worker 主动 HALT~~ / ~~Prompt 级门控为主~~ | 命令日志 `[CMD]`（覆盖有命令的 phase：pr-create/wt-create/a2a-exit）+ A2A input-required（尽力覆盖所有 phase） | Q18: 命令一定执行因此日志可靠，但 B1/B2/RED/dev/GREEN 无对应 CLI 命令，无法用 [CMD] 覆盖——这些 phase 依赖 prompt 指令 + reviewer 审核 |
| 状态名 | ~~blocked~~ | `input-required`（A2A 标准） | Q12: 对标 Google A2A |
| phase 检测 | ~~文件系统产物检测~~ | Reviewer 语义审核 | Q11: 文件检测不可靠，语义判断需要 Reviewer |
| 终止态 | ~~只有 completed/failed~~ | + `canceled` | Q12: A2A 标准三个终止态 |
| exit_kind | ~~内部概念~~ | 干掉，用 `--state` | Q12: A2A 协议没有 exit_kind |
| 指令路径 | ~~Reviewer → Manager → Worker~~ | Reviewer 直接对 Worker 发 GO/FIX | Q6: 减少一跳延迟 |
| Worker 怎么等 | ~~轮询 a2a state~~ | prompt 结束自然空闲，没有下一个 prompt | Q8/Q9: 协议层保证 |
| skills 配置 | ~~skills_path 文件路径~~ | supportedSkills（skill 名列表） | Q17: deploy-skills 管路径 |
| pr-review-guarded | ~~保留但去重~~ | 被 per-phase reviewer 替代 | Q7: 每 phase 已审，PR 级冗余 |

### 最终架构——三个 Agent 协作

```
manager_01 (develop wt) — 永不阻塞，daemon 循环
  │
  ├── cycle 轮询 a2a_tasks（30s 间隔）
  │   ├── state=input-required → 读 reason → dispatch（reviewer 或自己介入）
  │   ├── state=completed → wt-close
  │   └── 超时 → 告警
  │
  ├── worker_NN (fix|feature wt) — 每 phase 一个 ACP prompt
  │   │  prompt: "Do B1..." → 执行 → a2a-exit --state input-required
  │   │  prompt 结束 → session 空闲 → 等 reviewer_NN 的 GO/FIX prompt
  │   │  收到 "GO: B2" → 执行 B2 → a2a-exit --state input-required
  │   └── ...循环直到全部 phase 完成
  │
  └── reviewer_NN (fork manager_01) — 按需触发
      │  manager_01 dispatch → fork session → 审核 phase 产物
      │  读前置 phase 是否按序完成 → 读当前 phase 产出质量
      │  pass → PATCH worker state=working + session/prompt "GO: next"
      │  fail → PATCH worker state=working + session/prompt "FIX: ..."
      └── 回报 verdict 给 manager_01
```

### 完整状态机

```
submitted → working → input-required → working → ... → completed
                    ↘ failed                        ↘ canceled
```

| state 转换 | 谁可以 | 条件 |
|-----------|--------|------|
| submitted → working | manager_01 (via Runtime) | ACP session/fork 启动 Worker |
| working → input-required | worker_NN | phase 完成，a2a-exit --state input-required |
| input-required → working | reviewer_NN | GO/FIX verdict |
| input-required → working | manager_01 | need_clarification / blocked_by_env 回复（不经过 reviewer） |
| working → failed | worker_NN / manager_01 | 崩溃 / 超时 |
| any → canceled | manager_01 | 主动放弃 |
| any → completed | manager_01 | wt-close（唯一终章） |

**防重复 dispatch 守卫**：manager_01 cycle 检测到 `input-required` 后，先 PATCH task message 加 `review_assigned=reviewer_NN`。下轮 cycle 看到已有 `review_assigned` → 跳过。避免并发 race condition。reviewer 完成后清除 `review_assigned`。

### 候选拆分

预研中识别出以下独立 candidate。按依赖顺序排列：

```
Candidate A: #3639 a2a-state-standard（✅ 已完成 PR #3640 + cleanup #3642）
  └── state 标准化: input-required, canceled, --state ✅
  └── exit_kind 移除 ✅
  └── PENDING_INPUT 全量清理 ✅

Candidate B: #3638 supervisor-cycle-monitor（本 feature）
  ├── B1a: cycle framework（先做，可独立测试）
  │     └── freely cycle 命令 + a2a_tables 轮询
  │     └── state 检测 + 超时告警
  │     └── manager_01 daemon 循环
  │     └── 防重复 dispatch 守卫
  ├── B1b: reviewer + GO/FIX（依赖 B1a）
  │     └── worker_NN 逐 phase prompt 模板
  │     └── reviewer_NN fork + 语义审核
  │     └── GO/FIX 协议 + session/prompt
  │     └── a2a_tasks.message 结构化 JSON
  │     └── 异常恢复（crash / timeout / 连续 fail / session leak）
  └── 依赖 Candidate A

前置验证（B 启动前必须完成。BLOCKING：不通过则 B 方案基础动摇）：
  - ACP session/prompt 非自主继续假设验证：手动对 Worker session 发 session/prompt，
    确认 AI 在 response 后 session 空闲，不自发继续。
  - 如果验证失败（AI 自发继续）：B 方案需重新设计卡点机制。

Candidate C: agent-table A2A 对齐（后续）
  └── name, version, url, capabilities, supportedSkills
  └── agent-id.env 补 session_id
  └── session/fork vs prompt 决策逻辑

Candidate D: SSE 实时推送（Phase 2）
  └── Runtime SSE client
  └── 替代 polling
  └── SSE 事件 → ACP launch
```

**当前 candidate 范围**：Candidate A（先做）+ Candidate B（再做）。

### Q18（修正 Q9）: 卡点的真正机制——命令日志（准确）+ A2A state（尽力）

**核心洞察**：Agent 可能不执行 `a2a-exit`，但**命令一定会执行**。命令是 shell 脚本，在顶部打印标准化日志——100% 准确，不依赖 Agent 自律。

**Layer 1（兜底，命令级）：有命令的 phase 在命令顶部打印调用标记**

每个 Freely 命令（`pr-create-guarded`、`wt-create`、`a2a-exit` 等）在执行的**第一行**打印标准化日志：

```
[CMD] pr-create-guarded called, raw-key: 20260630T002621Z
[CMD] wt-create called, raw-key: 20260630T002621Z, kind: feature
[CMD] a2a-exit called, state: input-required, raw-key: 20260630T002621Z
```

Runtime 监控日志文件，grep `[CMD]` 行：
- 检测到 `pr-create-guarded` 执行 → 去 worktree 搜 IBM 文件
- 缺 `brainstorms.md`？→ 前置 B1 被跳过 → alert reviewer
- 缺 `pre-tests.md`？→ 前置 B2 被跳过 → alert reviewer

日志是**客观事实**——命令执行了就是执行了。Agent 不可能"偷偷"跳过命令。这就是 Agent Conveyor 的 cycle 检测原理——不是检测 Agent 意图，是检测**已发生的客观行为**。

**Layer 2（尽力，Agent 级）：A2A state input-required**

Agent prompt 仍然包含 `a2a-exit --state input-required` 指令。如果 Agent 执行了 → 标准 A2A 流工作。如果 Agent 没执行 → Layer 1 兜底。

```
Agent 做了 a2a-exit:
  → A2A state=input-required → manager_01 cycle 检测 → dispatch reviewer → 标准流程

Agent 没做 a2a-exit，但执行了 pr-create-guarded:
  → 日志捕获 [CMD] pr-create-guarded → 检查 IBM 文件 → 缺文件 → alert reviewer
  → reviewer 判断: Agent 跳过了 B1/B2/RED/dev/GREEN? 还是只是忘了写 a2a?
```

**为什么不找 worker 而找 reviewer**：

Worker 已经证明它会糊弄（跳过 B1/B2 直接 pr-create，或者 actual_RED_output 全填占位符）。让它"补文件"只会建空壳。必须独立 reviewer 判断。

**准确度对比**：

| 检测方式 | 依赖什么 | 覆盖范围 | 能抓到什么 |
|---------|---------|---------|-----------|
| Prompt 指令 | Agent 自律 | 全 phase（上限） | Agent 可能做也可能不做 |
| 命令日志 `[CMD]` | 命令一定打印 | 仅有命令的 phase（pr-create、wt-create、a2a-exit） | 命令被调用了 |
| IBM 文件存在 | 文件系统 | 有文件产物的 phase（B1/B2 有文件） | 文件存在（但内容可能假） |
| Reviewer 语义审核 | 独立 Agent | 所有 phase | 内容质量（最可靠但成本最高） |

**上限是 prompt 指令**。命令日志只能兜住有命令的点（pr-create、wt-create、a2a-exit）。B1/B2/RED/dev/GREEN 没有对应 Freely CLI 命令——Agent 写文件、编辑 pre-tests.md 不是命令调用。这些 phase 只能用 prompt 指令 + reviewer 审核。

### Q19: Watchdog 架构——命令→检查项→acp 介入

**关键时序**：`[CMD]` 日志在命令**开始执行时**打印，不是执行完后。所以：
- 检查的是**这个命令执行前应该已经达到的状态**（前置条件）
- ACP 发的 "STOP" 是语义信号——不会阻塞正在运行的命令，Worker 下个 turn 看到
- 比如 `[CMD] pr-create-guarded` 触发 → 检查 B1/B2/RED/dev/GREEN 是否已完成（应该在 pr-create 之前做完）

**设计原则**：每个命令对应一组**前置条件检查**。检查方法独立、可插拔、只检查"有没有"不检查"好不好"。

**架构**：

```
Watchdog 主循环:
  grep [CMD] 日志 → 提取 command + raw-key
  → 查 PRE_CHECK_MAP[command] → 得到前置条件检查列表
  → 逐个执行检查(raw-key)  ← 检查的是"这个命令执行前应该已经有的东西"
  → 全部 pass → 继续监控
  → 有 fail → 三步介入（ACP STOP 语义，不阻塞命令执行）
```

**命令→前置检查映射表**（PRE_CHECK_MAP）：

```
pr-create-guarded:          ← 执行前，以下应该全部完成
  check_b1_done            → brainstorms.md + candidates.md 存在?
  check_b2_done            → pre-tests.md + tasks.md 存在?
  check_red_executed       → pre-tests 全部 item red-green-status != pending?
  check_dev_done           → git diff base..HEAD 有代码变更?
  check_green_executed     → pre-tests 全部 item red-green-status = green?
  check_evidence_real      → evidence_file 存在且 >1 行?

a2a-exit --state input-required:
  check_message_valid      → message 是合法 JSON? phase 字段有效?

wt-create:                 ← 执行前，raw issue 应该已存在
  check_raw_issue_exists   → 平台上有 open issue?
  check_not_duplicate      → 同一 raw key 没有已存在的工位?

wt-close:                  ← 执行前，PR 应该已 merge
  check_pr_merged          → git log 有 merge commit? 分支已合并到 develop?
```

**每个检查方法的签名**：

```python
def check_b1_artifacts(worktree: str, raw_key: str) -> CheckResult:
    """检查 B1 产物是否存在"""
    brainstorms = glob(f"{worktree}/docs/pre-brainstorms/{raw_key}--*/brainstorms.md")
    candidates = glob(f"{worktree}/docs/pre-brainstorms/{raw_key}--*/candidates.md")
    if brainstorms and candidates:
        return CheckResult(passed=True)
    return CheckResult(
        passed=False,
        missing=["brainstorms.md", "candidates.md"],
        reason="B1 未完成：brainstorms.md 或 candidates.md 缺失"
    )
```

**职责分工**：Watchdog 只做检测+输出。Runtime 负责 ACP 委派链。

**关键桥梁——agent-id.env**：

```
[CMD] pr-create-guarded called, raw-key: 20260630T002621Z
         │
         ▼
agent-id.env:
  /path/fix-raw-20260630T002621Z-supervisor-cycle-monitor = worker = worker_03 = session_id = abc123
  /path/test-pre-merge-20260630T002621Z-supervisor-cycle-monitor = worker = worker_03 = session_id = def456
         │
         │  worktree 路径含 raw-key → 精确匹配
         ▼
  得到: agent_id = worker_03, session_id = abc123
         │
         ▼
  ACP session/prompt → session_id=abc123（精确定位，不是泛发"给 worker"）
  ACP session/fork → reviewer（查 agent-table 配对）
```

**完整链路**：

```
Watchdog:   [CMD] 日志(raw-key) → agent-id.env(session_id) → 查 PRE_CHECK_MAP → 输出
Runtime:    读到 [WATCHDOG] FAILED →
            1. ACP session/prompt <worker_session_id>:
               watchdog 完整输出（"请暂停，等进一步指令"）
            2. ACP session/fork → reviewer:
               watchdog 输出 + worker 上下文
            3. Reviewer verdict → ACP session/prompt <worker_session_id>:
               GO/FIX 新指令
```

**三步**（有 check fail 时。ACP STOP 是语义信号，不阻塞正在运行的命令）：

```
1. ACP session/prompt → worker_NN:
   "STOP. 你执行了 pr-create-guarded，但前置检查未通过:
    - B1 未完成: brainstorms.md 缺失
    - RED 未执行: red-green-status 仍为 pending
    当前命令完成后不要再继续。等待 reviewer 审核结果。"

2. ACP session/fork → reviewer_NN:
   "Worker 的 pr-create-guarded 触发 watchdog。
    前置检查未通过: [fail_details]
    请独立审核。审核后直接对 Worker 发 GO/FIX。"

3. Reviewer verdict → ACP session/prompt → worker_NN:
   "GO: 补充 B1 brainstorms + 重新执行 RED" 或 "FIX: ..."
   
   Worker 当前命令执行完后，下一个 turn 收到此消息 → 按指令继续。
```

**兜底能力上限**：只能检查"有没有"，不能检查"好不好"。brainstorms.md 存在但内容是"TODO"？检查 pass——需要 reviewer 语义审核判断。但至少不会放过"完全没做"的情况。

**非阻塞执行**：检查需要时间（读文件、grep、git log），不阻塞命令执行。命令照常运行，检查异步完成。结果在下个 cycle 或 ACP prompt 中传递。

**输出格式**（检查结果）：

```
[WATCHDOG] pr-create-guarded called, raw-key: 20260630T002621Z
[WATCHDOG] pre-condition checks (6 items):
  ✓ B1 done: brainstorms.md + candidates.md exist
  ✓ B2 done: pre-tests.md + tasks.md exist
  ✗ RED executed: 3/5 items red-green-status = pending
  ✗ GREEN executed: 0/5 items red-green-status = green
  ✓ dev done: git diff has code changes
  ✗ evidence real: acceptance-1.txt is 1 line (ghost pass)

[WATCHDOG] 3/6 checks FAILED
[WATCHDOG] pr-create-guarded 执行前应满足以下前置条件，但未满足：
  - RED 未执行: pre-tests 中 3 个 item 仍为 pending
  - GREEN 未执行: pre-tests 中 0 个 item 为 green
  - evidence 不真实: acceptance-1.txt 仅 1 行
[WATCHDOG] 请暂停，等进一步指令。
[WATCHDOG] 3/6 FAILED → Runtime ACP session/fork reviewer → reviewer verdict → ACP session/prompt worker
```

**后续能力提升**：发现新漏检模式 → 新增检查方法 → 加入 PRE_CHECK_MAP。不改架构，不增加延迟。

**扩展方式**：后续发现新的漏检模式 → 新增检查方法 → 加入 CHECK_MAP。不改架构。

**类比**：这就是 Freely 自身的门禁（gate）逻辑——不信任 Agent 自述，检查客观证据。`[CMD]` 日志就是 Runtime 的 gate check。

**Manager 也有自己的流程**：feedback → wt-create 是 Manager 的 phase，同样有 `[CMD]` 标记 + input-required 卡点。

### 补充说明（Reviewer 反馈）

**Q1/Q3 设计保持有效**：SessionReader 抽象层（ACP 探针注入 / Codex JSONL / a2a message 兜底）和 InterventionAdapter（nudge/interrupt/finish/get_status per tool）未被推翻，在 B1b 实现时需要。综合收敛未重复列出，但它们仍是有效设计。

**B1b 对 Candidate C 的独立性**：reviewer dispatch 可以始终使用 `session/fork`（不重用已有 session），先不依赖 agent-id.env session_id 逻辑。缓存命中率会降低但不阻塞功能。C 是优化项。

**Phase 1 交付范围**：Manager daemon cycle（B1a）在 Phase 1 内。Watchdog `[CMD]` 日志检测 + PRE_CHECK_MAP 在 Phase 1 内作为兜底层。两者都在 Phase 1。

**[CMD] 日志需改的命令列表**：
- `pr-create-guarded`、`pr-merge-guarded`、`wt-create`、`wt-close`
- `a2a-exit`（已有 `--state`）
- 文件：`bin/pr-create-guarded`、`bin/pr-merge-guarded`、`docs/system/workspace/scripts/worktree/wt-create`、`docs/system/workspace/scripts/worktree/wt-close`、`a2a_task.py` (a2a-exit)

**PRE_CHECK_MAP 与现有 gate 去重**：部分检查项与 governance-merge-gate / pretests-gate 重叠。Watchdog 的 PRE_CHECK_MAP 是**运行时实时检查**（命令执行时触发），gate 是**提交/合并时检查**（commit/merge 时触发）。时机不同、目的不同——不去重，并存。

**Worker prompt 模板位置**：存放在 `docs/system/workspace/agents/worker-agent.md` 中，作为 Worker agent 的标准 prompt 模板。Phase 实现时在此文件中定义逐 phase 指令格式。

### 已知风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| ACP session/prompt 非自主继续假设未验证 | **CRITICAL** | B 启动前手动验证：发 session/prompt → 确认 AI response 后 session 空闲 |
| Reviewer fork 缓存命中不稳定 | HIGH | Candidate C 补 agent-id.env session_id 字段 + session/prompt 复用 |
| Worker 长时间 tool call 无法中断 | MEDIUM | session/prompt 注入 `__FREELY_CHECKPOINT__` → Worker 下次 tool call 前检查。Phase 1 接受延迟，Phase 2 探索 session/cancel |
| Reviewer session leak（crash 后残留） | MEDIUM | wt-close Phase 4.5 扩展：不仅关 worker session，也关 reviewer session。agent-id.env 清理 |
| Worker crash 恢复不完整 | MEDIUM | crash → manager_01 PATCH state=input-required + message="worker crashed at phase X"。重新 session/fork Worker → prompt "resume from phase X"。依赖 worktree 文件系统状态重建上下文 |

**A 做完 B 才能用标准状态名，不需要自己发明 blocked。**

## Candidate
- candidate_id: C-20260630T002621Z-A
- status: promoted
- milestone: M-20260630T002621Z-A
