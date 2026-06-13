# Freely 项目意图

> 我是项目意图，指引方向，阐述为何而做。

## 核心目标

构建一个 Jarvis 式自主循环运行器：
- 启动后 AI 担任项目所有者角色。
- AI 从项目意图、story-scoped code-reviews、test、chat 输入与会话证据（人类或自治）、github-issue、治理漂移、运行时异常中发现新问题，并先收敛为 candidate；从 scan 结果获取待委派任务，从 a2a_tasks 表查询进行中任务；里程碑作为规划层追踪已纳入任务，从进度/恢复文档续接已有 issue；而非固定从单一任务列表
- AI 自主管理：获取 Issue → 文档 → 开发 → 验收 → 获取 Issue 的闭环
- AI 持续运行（自己监控ai工具崩溃/阻塞自动触发续接），除非明确停止。或找不到需求，或者出现重大事故 AI 自己已经无力自己解决。
- Freely 开发 Freely 时暴露的可复现共性问题，默认先判断是否应成为 Freely 能力发现；若可泛化到用户项目，应进入三个 loop 的 canonical lifecycle materialize 为可复用能力，而不是停留成一次性项目经验。

## Freely 产品/系统架构

Freely 自身首先是一个产品，不应被拆成一堆并列的 shell、命令和工具名。

当前高层关系定义为：

- `Freely product`
  - `Freely core`
  - `Freely CLI`
  - `Freely TUI app`
  - `Freely GUI app`

其中：

- `Freely core`
  - runtime / orchestration
  - service contract / adapter boundary
  - external AI tooling orchestration
  - eval / harness / operational substrate
- `Freely CLI`
  - `Freely core`
  - CLI command set
- `Freely TUI app`
  - `Freely core`
  - TUI shell
- `Freely GUI app`
  - `Freely core`
  - GUI shell

还要显式区分两类不应再和 shell 并列的东西：

1. semantic surfaces
   - `init`
   - `start`
   - `chat`
   - `baseline-status`
   - `live-status`
   - `fleet-status`
2. external AI tooling layer
   - `codex`
   - `Claude Code`
   - MCP-assisted tool usage
   - 其他被 Freely 编排的外部 AI tools

原则：

- `chat` / `status` family 是 Freely 通过 shell 暴露的语义面，不是 shell 自身。
- `CLI shell`、`TUI shell`、`GUI app` 是宿主壳，不是业务语义本体。
- 外部 AI tools 是 Freely core 编排的执行提供层，不是 Freely 自己的 product shell。
- 若未来要沉淀“通用产品形态方法”，应另开独立 lifecycle；本节只表达 Freely 自身产品架构。

## 方法论总述

### 三个 Loop 方法论

说明：
- 本节只定义 Freely 为什么需要三个 loop，以及高层闭环原则。
- `docs/system/workspace/three-loop-capability-lifecycle.md` 是 whole-app lifecycle / logic 的唯一细节真源。
- 因此本文件不再重复维护 three-loop 的细节图、route map、artifact 流转和 terminal semantics；这里只保留高层定位与引用约束。
- 任何会改变 three-loop routing、loop placement、completion / verification / cleanup / recovery judgment 的实现、prompt 或文档，在修改前都必须先阅读并理解该真源；若语义变化，必须同步检查并按需更新该真源。

高层定位：
- `auto-loop` 是 outer orchestration / governance loop
- `doc-loop` 与 `dev-loop` 是 sibling execution loops
- verification / recovery / cleanup 是 route、phase 或 governance path，不是新增 loop
- worker 在 `doc-loop` / `dev-loop` 中产出 evidence；completion / verification / cleanup / retirement judgment 回到 `auto-loop`

### 来源与路由规则

说明：
- 本节只保留高层方向性约束，不再平行维护来源到具体 skill / route_kind / return path 的细表。
- 详细 capability -> loop -> owner -> artifact -> transition 映射以 `docs/system/workspace/three-loop-capability-lifecycle.md` 为准，不在本文件重复展开。
- 高层上，新问题与边界未稳的问题先进入 `doc-loop` 收敛；已收敛 issue 在 `doc-loop` 完成 B2_IBM 后进入 `dev-loop` materialize；completion / verification / cleanup / recovery judgment 统一回到 `auto-loop`。
- 其中 `dev-loop` 是 AI-native 能力实现层，不限于传统“写代码”；凡是在既有 issue 边界内把能力真正 materialize 出来的工作，都属于 `dev-loop`。

流程标识词典与状态联动矩阵的规范语义统一见 `docs/LAWS.md` 第 2C 章；其中 issue / progress 的主执行标识统一使用 `phase_state`，skills 与 milestone policy 不得再自行发明同名状态。

### Chat 输入与会话证据（人类/自治）

```
人类 ←──→ Chat Session ←──→ AI
              │
              ├── 讨论先进入 B1_IBM：沉淀到 pre-brainstorms/*/brainstorms.md
              ├── candidate 写入 pre-brainstorms/*/candidates.md（B1_IBM 产物，进入 milestone）
              ├── 多 AI/子代理会话日志以 jsonl 作为 session evidence
              └── 在 candidates.md / issue / progress / recovery 中持续维护 `session_refs`
```

说明：
- `session_refs` 至少记录 `tool`、`session_id`、`jsonl_path`、`role`
- 若当前工具无法暴露 jsonl 路径，允许 `jsonl_path=unavailable://<reason>`，但不得省略 `session_id`

### 闭环理念

```
文档指导开发 → 开发反馈文档 → 循环直到完成
     ↑                              │
     └────────── 闭环 ──────────────┘
```

## 操作模式

1. **宪法约束的自主性**
   - 宪法是硬性约束面
   - 分支/工作树规则、技术栈约束、方法论约束

2. **单会话运行**
   - 每个运行实例拥有一个活动 AI CLI 进程/会话
   - 监控目标：该进程/会话生命周期

3. **恢复优先的连续性**
   - 支持无人值守续接时直接续接
   - 不支持时执行桥接步骤：更新进度文档，重启无人值守循环

4. **最小输入面**
   - 四个必需输入：
     - 项目绝对路径
     - 项目意图路径
     - 宪法路径
     - AI 规格 `tool:model:mode`
   - AI 自主发现其他项目文档

## Freely 产品/系统架构总览

这一节只回答 Freely 自身作为产品时的高层架构，不定义 Freely 未来给其他应用复用的通用产品形态方法。

### 产品壳与核心

Freely product 由以下部分组成：

- `Freely core`
- `Freely CLI`
- `Freely TUI app`
- `Freely GUI app`

其中：

- `Freely core`
  - 负责 runtime orchestration、external AI tooling orchestration、service contract、state/evidence、three-loop routing
- `Freely CLI`
  - 是 Freely 当前的 canonical product shell
  - 通过 CLI command set 暴露 front-door、observability 与 control semantics
- `Freely TUI app`
  - 是 terminal-hosted shell
  - 若存在，只能复用同一 core 与 backend contract
- `Freely GUI app`
  - 是 graphical shell
  - 若存在，只能复用同一 core 与 backend contract

### 纵向架构

Freely 自身产品/系统架构的当前高层拓扑可理解为：

1. operational substrate
2. evaluation harness
3. autonomy evals / acceptance
4. external AI tooling layer
5. Freely runtime / orchestration
6. service contract / adapter layer
7. host shells

对应含义：

- external AI tooling layer
  - `codex`
  - `Claude Code`
  - MCP-assisted tool paths
  - 这些是 Freely 借力的 external AI tooling，不是 Freely 自身产品壳
- Freely runtime / orchestration
  - `freely` runtime scripts
  - manager / worker / lead
  - three-loop routing
  - continuity / patrol / queue / recovery
- service contract / adapter layer
  - backend contract
  - transport / adapter taxonomy
- host shells
  - CLI
  - TUI app
  - GUI app

### 正交语义面

下列概念不是和 `CLI shell`、`TUI shell`、`GUI app` 并列的产品壳，而是跨壳暴露的 semantic surfaces：

- boot semantics
  - `init`
  - `start`
  - `daemon start|stop|status|logs`
- submit / intervention semantics
  - `chat`
  - future human interruption submit paths
  - pause / retry / resume 等 control actions
- observability semantics
  - `baseline-status`
  - `live-status`
  - `fleet-status`
  - deeper session / stream / artifact references

因此：

- `chat` 不是 `CLI shell`、`TUI shell`、`GUI app` 的 peer
- status family 也不是 `CLI shell`、`TUI shell`、`GUI app` 的 peer
- foreground `start` 与 explicit `daemon` control plane 是同一 runtime/orchestration 的两种入口语义，不是两套并列产品壳
- `CLI shell`、`TUI shell`、`GUI app` 是承载这些语义面的 host shells
- Freely 自身的 `CLI-first` 选择，是 Freely 产品架构决策，不自动等于 Freely 通用能力

## 非目标

- 不是静态待办列表执行器
- 不是一次性命令运行器
- 不是人类驱动的工单机器人
<!-- runtime-lifecycle-validation -->
