# Issue: internal-frontend-backend-architecture-review

- issue_id: `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- phase_state: `in_ibm`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `internal-frontend-backend-architecture-review`
- issue-name: `internal-frontend-backend-architecture-review`
- source_candidate: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md#c-20260308-1244-01`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
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
