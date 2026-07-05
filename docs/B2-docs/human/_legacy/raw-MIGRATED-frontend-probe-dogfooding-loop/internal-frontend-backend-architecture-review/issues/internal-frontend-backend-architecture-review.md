# Issue: internal-frontend-backend-architecture-review

- issue_id: `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `internal-frontend-backend-architecture-review`
- issue-name: `internal-frontend-backend-architecture-review`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260308/candidates.md#c-20260308-1244-01`
- source_brainstorm: `docs/B1-docs/raw-20260308/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]

## Why

重新评审 Freely 当前产品形态下的前后端边界，确保：

- “前后端”首先是一种内部解耦思想，而不是 day-1 就要求远端服务化
- Freely 可以先作为带终端的桌面开发工具落地，但内部仍保持明确 frontend/backend 边界
- 协议层从第一版开始可插拔，不把 UI 和 backend 绑定到单一 transport
- 后续切换到 WS、sidecar 或远端服务时，不需要推翻第一版 Frontend Probe
- 人类在 loop 中默认不阻塞，但依然拥有高优先级纠偏入口
- UI 要把多个 AI 执行单元呈现成“一个团队”，让人能观察谁在做什么、做到哪一步、是否阻塞

## Scope

1. 明确 Tauri 桌面工具内部的 frontend / backend 职责边界。
2. 明确哪些状态由 frontend 持有，哪些状态必须由 backend 持有。
3. 收敛 day-1 命令面、事件流和快照面。
4. 定义可插拔协议分层：
   - frontend contract
   - transport adapter
   - backend service contract
5. 约束第一阶段技术栈与运行时：
   - Rust
   - Tauri
   - Bun
   - React
   - TypeScript
   - 不引入 Node.js 作为产品运行时
6. 定义“Freely 何时达到可自治开发并开始自己开发自己”的 MVP 里程碑。
7. 定义人类控制面：
   - 启动
   - 暂停
   - 终止
   - resume
   - chat input 介入
8. 定义多输入源优先级模型，至少覆盖：
   - human chat input
   - auto-loop generated actions
   - recovery / monitor signals
   - system-triggered governance events
9. 定义 AI 团队态势 UI 的最小展示模型。

## Acceptance

- issue-bound 文档明确 day-1 形态下的 frontend/backend 边界，不把“边界”误写成“必须远端 HTTP 化”。
- issue-bound 文档明确 `ClientCommand`、`ServerEvent`、`Snapshot` 的协议分层语义。
- 文档明确 transport adapter 可替换，至少覆盖 `tauri_adapter` 与未来 `ws_adapter` 的兼容原则。
- 文档明确 terminal、session、run、governance、skill routing 分别归属 frontend 还是 backend。
- 文档明确当前技术栈为 Rust + Tauri + Bun + React + TypeScript，且不依赖 Node.js 产品运行时。
- issue-bound 文档明确一个可验收的 `MVP autonomy milestone`，用于判断 Freely 何时可以开始自治开发并狗粮开发自己。
- issue-bound 文档明确 day-1 主入口是应用内终端 / 控制台，而不是外部 shell。
- issue-bound 文档明确 human chat input 拥有高于普通自治事件的纠偏优先级。
- issue-bound 文档明确最小 AI 团队态势 UI：至少能看到每个 agent / run 的状态、阶段、最近动作、阻塞原因、输入来源。

## Boundary model

### Frontend owns

- view-local state：面板开合、选中的 tab、临时输入草稿、过滤条件
- optimistic interaction state：按钮 loading、表单提交中、局部错误提示
- presentation composition：把 session / run / agent / timeline / terminal 组合成可观察界面
- route-level intent：用户正在看哪个项目、哪个 session、哪个 agent

### Backend owns

- project registry 与当前 active project
- session lifecycle、run lifecycle、agent roster、terminal/PTY lifecycle
- laws / routing / skill invocation 决策结果
- durable event log、history、snapshot、resume context
- input arbitration 结果与系统级治理事件

### Shared contract rule

- frontend 不直接持有运行事实，只消费 backend 发布的 `Snapshot` 与 `ServerEvent`
- frontend 可以缓存最近一份 `Snapshot` 以优化渲染，但缓存不是事实源
- backend 不关心具体 UI 布局，只提供可被不同 transport 复用的命令、事件和快照语义

## State ownership matrix

| Domain | Frontend | Backend |
|--------|----------|---------|
| project selection | 当前界面选中项 | 可执行项目列表、active project 事实 |
| session | 当前打开的 session panel | session 创建、恢复、历史、状态 |
| run | 视图聚合与排序 | run 生命周期、阶段、阻塞、恢复 |
| agent | roster 展示与筛选 | agent 标识、角色、最近动作、当前状态 |
| terminal | viewport、滚动、tab 聚合 | PTY 进程、输出流、退出码、attach/resume |
| governance | 呈现检查结果 | `AGENTS/CONSTITUTION/LAWS` 读取、规则判定、skill 路由 |
| chat intervention | 输入框与交互反馈 | 优先级仲裁、命令入队、执行结果留痕 |

## Protocol layering

### 1. Frontend contract

- 只定义 frontend 可调用的 `ClientCommand`
- 只定义 frontend 可订阅的 `ServerEvent`
- 只定义 frontend 首屏与恢复所需的 `Snapshot`
- 不暴露 transport 细节，不要求 HTTP/WS/Tauri 三选一

### 2. Transport adapter

- `tauri_adapter` 负责把应用内 command/event 桥接到 Rust backend
- 未来 `ws_adapter` 负责远端或多进程场景
- adapter 只能转换传输形态，不能改动业务字段语义
- adapter 必须保留 request correlation、stream ordering 和 error surface

### 3. Backend service contract

- 接收 `ClientCommand`
- 产出 `ServerEvent`
- 维护可重建 UI 的 `Snapshot`
- 对 session/run/agent/governance 作为唯一事实源

## Minimal protocol objects

### ClientCommand

- `CreateOrResumeSession`
- `SendChatIntervention`
- `ControlRun`：`start | pause | terminate | resume | retry`
- `AttachTerminal`
- `RequestSnapshot`

要求：
- 每条命令都必须带 `project_id`
- 涉及既有实体时必须带 `session_id` 或 `run_id`
- 命令来源必须可追溯，例如 `human-chat`、`human-control`、`auto-loop`

### ServerEvent

- `SessionUpserted`
- `RunStatusChanged`
- `AgentStatusChanged`
- `TerminalChunkAppended`
- `GovernanceDecisionRecorded`
- `InputArbitrationRecorded`
- `RecoveryStatusChanged`

要求：
- 事件必须单调追加，允许 UI 增量回放
- 事件至少带 `event_id`、`occurred_at`、`project_id`
- 事件语义独立于 transport

### Snapshot

- 当前 project 概览
- active sessions / runs / agents 摘要
- terminal attach target 摘要
- 最近 governance / recovery / blocker 摘要
- UI 恢复所需的最后已知事实

要求：
- `Snapshot` 用于首屏和重连恢复，不替代完整 history
- `Snapshot` 必须能从 backend 当前状态重建，不依赖 frontend 私有缓存

## Input arbitration

优先级从高到低：

1. 显式控制命令：`terminate`、`pause`、`resume`
2. `human chat input`
3. recovery / monitor signals
4. system-triggered governance events
5. auto-loop generated actions

约束：

- 高优先级输入必须可抢占低优先级待执行动作
- 仲裁结果必须写成 backend event，不能只停留在 UI 上
- 被抢占动作必须保留可追溯原因

## Day-1 UI contract

- `control bar`：只调用 `ControlRun`
- `chat intervention panel`：只调用 `SendChatIntervention`
- `agent roster`：只消费 agent/run snapshot 与状态变更事件
- `team timeline`：只消费 event log，不拼接隐式推断事实
- `embedded terminal`：通过 `AttachTerminal` + `TerminalChunkAppended` 组合

## Exit criteria for `done_ibm`

- 本 issue 已明确 frontend/backend 边界、状态归属矩阵和协议分层
- 已冻结 `ClientCommand`、`ServerEvent`、`Snapshot` 的最小对象族
- 已明确 `tauri_adapter` 是 day-1 adapter，而不是业务协议本体
- 已明确输入仲裁与 team visibility 的最小 contract
- 后续 `Frontend/Backend Boundary Contract v1 for Frontend Probe` 可以直接基于本 issue 继续细化接口，不需要重新争论边界归属

## MVP autonomy milestone

当且仅当以下能力同时成立，Freely 才算达到“可以开始自治开发自己”的 MVP：

1. `Frontend Probe` 可用
   - 可选中项目
   - 可创建或恢复 session
   - 可发送消息
   - 可看到流式输出与终端输出
   - 可 stop / retry / resume
   - 可在应用内终端里发起启动，而不是依赖外部 shell
2. `Backend boundary contract` 可用
   - 支持最小 `ClientCommand`
   - 支持最小 `ServerEvent`
   - 支持最小 `Snapshot`
   - transport adapter 可先落在 `tauri_adapter`
3. `Governance as features` 可用
   - 应用可读取当前项目的 `AGENTS.md`、`CONSTITUTION.md`、`LAWS.md`
   - 应用可发现 system skills
   - 一次用户或 AI 动作会先经过 laws / routing 判断，再进入 skill
4. `Single-issue dev loop` 可用
   - Freely 能在受管项目中选取一个明确 issue
   - 在正确 worktree 中执行一次最小开发循环
   - 能把执行状态和结果回流到 Frontend Probe
5. `Human correction loop` 可用
   - 人能在运行中观察
   - 人能在运行中打断
   - 人能在中断后重新发指令并继续
   - human chat input 具有高于普通自治事件的纠偏优先级
6. `AI team visibility` 可用
   - 人能看到多个 AI agent / run 的当前状态
   - 人能看到每个 agent 当前阶段和最近动作
   - 人能看到阻塞 / 恢复 / 等待中的原因
   - 人能像看一个团队一样理解整体推进情况

达到以上 6 条后，Freely 就不再只是“能跑脚本”，而是已经具备最小自治开发闭环，可以开始用 Freely 开发 Freely。

## IBM Handoff

- current_status: `done_ibm`
- why_now: 本轮首跳重扫后，`docs/milestones.md` 中更早的两个 committed issue 仍停在 `in_verification` 且 blocker 已收敛为 ownership split；相比之下，`I-20260308-1245` 仍是当前可继续推进的 milestone-owned issue。
- selected_tool: `codex`
- target_skill_or_loop: `skill:doc-ibm-execution`
- why_selected_tool: 当前工作是仓库内 issue-bound 文档收敛与里程碑回写，`codex` 更适合直接修改现有 IBM 产物，且与当前 `AI_TOOL` 一致。
- next_prompt: `继续承接 I-20260308-1245 的 issue-bound IBM 收口。确认 frontend/backend 边界、状态归属矩阵、协议分层、ClientCommand/ServerEvent/Snapshot、input arbitration、team visibility 与 MVP autonomy milestone 已足够驱动后续接口细化；把 issue 与 milestone 从 in_ibm 推进到 done_ibm，并把下一跳指向 Frontend/Backend Boundary Contract v1 的 issue-bound materialization。`

## Verification

- `rg -n "ClientCommand|ServerEvent|Snapshot|tauri_adapter|ws_adapter|frontend contract|transport adapter|backend service contract|MVP autonomy milestone|Input arbitration|AI team visibility" docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy -g '*.md'`
- `rg -n "I-20260308-1245|internal-frontend-backend-architecture-review" docs -g '*.md'`
- `./bin/governance-check`

## Closure Judgment

- 本 issue 的交付物是前后端边界、协议分层、输入仲裁与团队态势 UI 的总体 contract freeze，而不是具体 probe 或 bridge 实现；这些边界已经在当前 issue 中完整冻结。
- 下游 `Frontend/Backend Boundary Contract v1 for Frontend Probe` 与后续 control-surface contract 文档已经直接引用并复用这条边界，说明它已成为 canonical architecture truth source，而不再只是 IBM 中间态。
- 因此 `I-20260308-1245` 可以按真实写回推进到 `completed`；后续 frontend probe、runtime baseline 与 bridge 联调继续沿这条边界推进，不回灌到本 issue 重开总论。

## Next

- 当前 issue 已完成 canonical closeout，后续 Probe v1/v0、runtime baseline 与 bridge work 直接复用该边界；若未来需要改写更高层系统拓扑或自治 milestone 定义，另开新的 lifecycle。

## Human interaction policy

- 人类默认不阻塞主自治循环。
- 人类输入属于 side-channel，但不是低优先级噪声。
- `chat input` 必须作为高优先级纠偏输入处理。
- `pause` / `terminate` / `resume` 属于显式控制命令，优先级高于普通自治动作。
- 系统需要记录输入来源与仲裁结果，避免“谁打断了什么”不可追溯。

## AI team visibility

day-1 UI 不应只展示一条日志流，而应至少提供：

1. `control bar`
   - start
   - pause
   - terminate
   - resume
2. `chat intervention panel`
   - 人类输入框
   - 输入优先级提示
   - 最近一次介入结果
3. `agent roster`
   - 每个 agent / run 的名称或标识
   - 当前状态
   - 当前阶段
   - 最近动作
   - 最近事件时间
4. `team timeline`
   - 关键事件流
   - 进展推进
   - 阻塞 / 恢复 / handoff
5. `embedded terminal`
   - 当前执行的终端输出
   - 需要时可切换到具体 agent / run

该布局目标不是模仿传统 IDE，而是让人像观察一个 AI 团队那样理解当前系统。

## Next

- 在本 issue 完成 `done_ibm` 后，再进入：
  - `Frontend/Backend Boundary Contract v1 for Frontend Probe`
  - `Frontend Probe v0`
