# 研究：Freely 架构综述与 API / Adapter 边界统一

## Context

- 日期：2026-03-12 00:11 UTC
- 触发：重新系统梳理 Freely 当前所有架构相关文档，判断产品形态、内部前后端边界、协议层、runtime 替换面、第三方接入面之间是否已经形成一致架构。
- 研究目标：不是重复已有单点结论，而是把分散在 CLI 编排、前后端解耦、Frontend Probe、OpenClaw 可行性、EvoMap 生态研究中的架构结论统一成一个更高层的总图。

## 本次阅读范围

核心规范：

- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`

架构主文档：

- `docs/B1-docs/raw-20260303-0000/brainstorms.md`
- `docs/B1-docs/raw-20260304-0000/brainstorms.md`
- `docs/B1-docs/raw-20260308-1244/brainstorms.md`
- `docs/B2-docs/human/tui/prd.md`
- `docs/B2-docs/human/tui/issues/internal-frontend-backend-architecture-review.md`

第三方生态与扩展研究：

- `docs/B1-docs/raw-20260304-0000/brainstorms.md`
- `docs/B1-docs/raw-20260304-0000/brainstorms.md`
- `docs/B1-docs/raw-20260304-0000/brainstorms.md`

## 先给统一结论

Freely 当前真正收敛出的产品，不是单纯的 CLI 工具，也不是“先做个 Tauri 壳再说”的桌面应用，而是一个有明确内部分层的自治工程控制面：

1. `Frontend shell`
   - Tauri + React + TypeScript + Bun
   - 负责交互、观测、打断、回放、团队态势展示
2. `Boundary / protocol layer`
   - 用 `ClientCommand`、`ServerEvent`、`Snapshot` 表达稳定语义
   - 让 Tauri、WS、sidecar、本地进程、第三方 runtime 都只作为 adapter
3. `Backend service core`
   - Rust 持有 session / run / agent / terminal / governance / recovery 的事实状态
   - 负责自动循环、规则判定、状态持久化、恢复与执行编排
4. `Execution runtime adapters`
   - 本地 CLI tool、未来远端服务、OpenClaw profile、其他 runtime
   - 可替换，但都不应成为产品语义本体

换句话说：

- Freely 的主产品是“自治软件工程控制面”
- Tauri 是 day-1 容器，不是产品本体
- CLI 编排是当前主要执行策略，不是唯一永久形态
- OpenClaw / EvoMap / 其他生态应被视为可插拔外部能力或 runtime 借力对象，而不是 Freely 的主定义

## 一、当前架构已经形成的稳定共识

### 1. Freely 的前后端分离首先是事实边界，不是部署边界

这一点已经在最新 IBM 中基本定型：

- frontend 只拥有 view-local state 与交互状态
- backend 才是 project / session / run / agent / terminal / governance / recovery 的事实源
- day-1 即使同进程同应用，也要先把事实边界切开

这说明“前后端分离”不是为了强行远端服务化，而是为了保证：

- UI 不直接侵入执行内核
- transport 可替换
- 后续迁移到多进程、守护进程、远端 backend 时不推翻第一版

### 2. 协议层已经有了正确方向，但还停在文档级冻结

目前最清晰的共识是：

- 前端不直接依赖 Rust/Tauri API 细节
- 中间应该冻结为三类对象：
  - `ClientCommand`
  - `ServerEvent`
  - `Snapshot`
- `tauri_adapter` 只是 day-1 adapter
- 未来可以有 `ws_adapter`、`local_process_adapter`，乃至其他第三方 adapter

这意味着 Freely 的真正 API，不应先被理解为 HTTP route 列表，而应先被理解为“稳定语义层”。

### 3. CLI 编排仍然是当前最可执行的内核路径

20260303 的研究和后续 `PROJECT_INTENT` 已把主链路定在：

- `external AI CLI tool`
- `lead-agent`
- `context-source-skill`
- `doc-pre-brainstorm-execution | doc-ibm-execution | dev-loop-execution`

这条路径仍然成立，因为它具备：

- 最低实现成本
- 对现有外部 AI 工具的复用能力
- 研究优先阶段可快速验证自治闭环

因此短期内，“Rust backend service core”并不等于立刻替换外部 CLI 工具，而是：

- 先负责 orchestration / state / governance / PTY / recovery
- 执行智能体仍可借助现有 AI CLI

### 4. Frontend Probe 不是附属品，而是自举验证能力

最新前端研究已经把一个关键风险说透：

- 如果只有后端和脚本，没有前端探针，人类无法及时发现 AI 跑偏
- Freely 自己要狗粮开发自己，就必须让每个后端增量都能被前端立即验证

所以现在更准确的路线不是“backend-first”，而是：

- `backend-core-first`
- `frontend-probe-from-day-1`
- `dogfooding-validation-per-increment`

这意味着前端并不是“等后端都做完再补”的下游工程，而是治理闭环的一部分。

### 5. UI 不应退化成单终端镜像，而应成为 AI 团队控制面

这轮补充讨论把前端的重要性又上推了一层：

- Freely 会被用户安装在不同操作系统上，作为一个完整应用使用
- 用户不是只想“看一段 CLI 输出”，而是要同时理解多个 worktree、多个 AI、多个 subagent 的推进状态
- 因此 UI 的任务不是把终端搬进桌面，而是把自治工程团队的状态结构化呈现给人

结论：

- terminal 仍然重要，但它更像可附着的工作面
- chat 仍然重要，但它不能吞掉整个产品布局
- Freely 的 UI 核心应是 team visibility，而不是单线程消息流或单一黑窗

## 二、当前文档之间仍然存在的架构张力

### 1. “Backend API” 这个词仍有歧义

有些旧研究里的 `Backend API` 更像网络 API 草案，例如：

- `POST /sessions`
- `GET /sessions`
- `GET /status`

这类表达适合作为未来 adapter 参考，但如果把它当成当前的规范主语，会过早把架构收窄成 HTTP/WS 服务。

更稳的说法应是：

- 先冻结 backend service contract
- 再决定 day-1 通过哪种 transport 暴露

### 2. “OpenClaw 借力” 和 “Freely 自建控制面” 之间还没有统一主从关系

现有研究对 OpenClaw 的判断是务实的：

- 它适合作为短期借力 runtime
- 但 Freely 的 supervisor、最小输入面、Git/worktree 强治理并不原生等价于 OpenClaw

这意味着：

- OpenClaw 不能成为 Freely 的总架构前提
- 更合理的定位是 `runtime adapter/profile`
- Freely 必须先定义自己的 product contract，再判断哪些 runtime 能适配

### 3. 技术栈事实源还没有按分层落地

当前规范层已冻结技术栈：

- frontend: React + TypeScript + Bun + xterm.js
- desktop shell: Tauri
- backend core: Rust + Rust PTY

但 manifest 仍未落地，因此现在的技术栈事实主要在文档里，而不是代码里。

这带来两个后续要求：

1. 前端 `package.json` 只能承载 frontend shell 依赖
2. backend 依赖必须留在 Rust manifest
3. 协议层对象不应埋进任一端的私有依赖清单
4. agent tooling / external CLI 也不应混进产品运行时依赖

### 4. “Freely 以 skill 暴露能力” 与 “OpenClaw workspace 可扩展” 可以形成互补关系

这轮讨论也把 OpenClaw 的位置重新压回了合适层级：

- OpenClaw 不是 Freely 的主架构
- 但它在 workspace 自定义、skills、memory、hooks 这些能力上，确实提供了一个很强的借力面

更合理的关系不是“Freely 依赖 OpenClaw 才成立”，而是：

- Freely 先定义自己的能力和治理语义
- 这些能力优先以 skill 暴露
- 对接 OpenClaw 时，再把这些能力投影到 OpenClaw 的 workspace 自定义面

这样做的价值是：

- 保留 Freely 的产品独立性
- 借用 OpenClaw 的记忆和工作区扩展优势
- 避免为短期借力而污染 Freely 的内核边界

## 三、基于现有研究，Freely 的推荐总架构

### 1. Product architecture

```text
Freely App / Control Surface
  -> Frontend shell
  -> Boundary contract
  -> Backend service core
  -> Runtime adapters
  -> External AI tools / ecosystem integrations
```

### 1A. 组件级落地架构

更贴近实现的 day-1 组件图，应先按下面这层拆开：

```text
Tauri Desktop Shell
  -> React Frontend Control Surface
     -> Frontend state store (view-local only)
     -> Boundary client
        -> tauri_adapter (day-1)
           -> Rust Backend Service Core
              -> project/worktree registry
              -> session/run orchestration
              -> governance + laws enforcement
              -> recovery coordinator
              -> terminal/PTy manager
              -> event log + snapshot builder
              -> AI tool adapter layer
                 -> codex adapter
                 -> iflow adapter
                 -> kiro-cli adapter
```

day-1 的关键是：

- 前端只持有 view state
- 后端持有运行事实
- `tauri_adapter` 只负责 transport
- AI 工具适配层只负责把 Freely 的执行语义投影到各家 CLI

### 1B. 当前主实现与未来增强的边界

为了避免预研把目标态写成已落地能力，建议显式分成两层：

`current-primary-path`

- Tauri 桌面壳
- Rust backend service core
- `tauri_adapter`
- 外部 AI CLI (`codex` / `iflow` / `kiro-cli`)
- Freely 自己的 skills / runtime / governance / worktree discipline

`future-enhancements`

- `ws_adapter`
- `openclaw_profile` / `openclaw_adapter`
- 更强的 memory backend
- direct interrupt intervention transport
- 更丰富的 AI team visibility 聚合模型

### 2. Boundary contract

`Boundary contract` 应负责冻结：

- command model
- event model
- snapshot model
- request correlation
- ordering guarantees
- error surface
- recovery surface

它不应直接绑定：

- HTTP path
- Tauri invoke/event 细节
- 某一个第三方 runtime 的字段命名

### 3. Backend service core

后端核心应长期持有这些职责：

- project registry
- session lifecycle
- run lifecycle
- agent roster
- PTY / terminal lifecycle
- governance decision engine
- routing / skill invocation orchestration
- recovery / resume context
- durable event log / snapshot rebuilding

这部分不应被前端、Tauri adapter 或第三方 runtime 反向定义。

### 3A. Backend service core 的模块切分建议

如果继续往实现落，backend 至少可以先切成这些模块：

1. `project_service`
- 当前项目注册
- 当前 active project
- project 对应的治理文档入口

2. `workspace_service`
- worktree 发现
- 分支/worktree 上下文
- execution base / integration target / depends_on

3. `session_service`
- session 建立与恢复
- session refs 留痕
- run 与 session 的绑定

4. `run_service`
- 当前阶段
- tool/model/mode
- 当前运行状态
- stop / retry / resume 控制

5. `terminal_service`
- PTY 进程
- terminal attach target
- 输出流与退出码

6. `governance_service`
- `CONSTITUTION` / `LAWS` / `AGENTS`
- 路由前置门禁
- intervention arbitration

7. `recovery_service`
- 崩溃检测
- resume / restart 决策
- recovery context 写回

8. `tool_adapter_service`
- `codex`
- `iflow`
- `kiro-cli`
- 未来其他 CLI / runtime adapter

### 4. Runtime adapter model

可预期的 adapter 至少有：

- `tauri_adapter`
- `ws_adapter`
- `local_process_adapter`
- `openclaw_adapter` 或 `openclaw_profile`

它们都应满足同一条原则：

- 负责承载和映射
- 不负责重新发明业务协议

### 4A. AI 工具适配层的当前技术判断

按当前仓库脚本与本机 CLI 能力，day-1 适配层可以先按下面分工：

- `iflow`
  - 研究/路由/文档型收敛优先
  - 擅长长 prompt、continue/resume
- `codex`
  - 仓库内实现、改文件、验证优先
  - 擅长 worktree 内开发闭环
- `kiro-cli`
  - 保留为可接入执行工具
  - 当前接入深度暂不应超越前两者

这意味着：

- 预研阶段的“技术栈”不只是前后端框架，还包括 AI tool stack
- 但 AI tool stack 应被视为 execution adapter，不是产品 runtime 本体

### 4B. 人类介入 transport 的当前主实现

这里也需要明确当前主路径，避免未来误以为必须先做“运行中实时插话”：

- 上层 contract 保留 `SendChatIntervention`
- 当前主实现优先走：
  - 停下当前 run
  - 保留 `tool/session_id`
  - 用 resume + intervention prompt 继续
- 未来若某些 CLI/SDK 支持 direct interrupt，再在 adapter 层升级

因此：

- `resume_with_intervention` 是当前主设计
- `direct_interrupt` 是预留能力，不是当前架构成立前提

### 4C. Human intervention transport 的统一 contract

为了让 UI、backend 与 AI tool adapters 不被厂商差异绑死，这里应进一步收紧成一个统一接口层：

`SendChatIntervention`

最小输入：

- `project_id`
- `session_id` 或 `run_id`
- `message`
- `source=human-chat`

最小输出：

- `accepted`
- `transport_mode`
- `result_state`

建议值：

- `transport_mode`
  - `resume_with_intervention`
  - `direct_interrupt`
- `result_state`
  - `queued_for_resume`
  - `delivered_live`
  - `rejected`

当前 day-1 的技术判断应明确为：

- 不要求各家 CLI 现在就支持运行中实时插话
- 当前主链先走 `resume_with_intervention`
- 只要上层 contract 稳定，未来才能无痛升级到 `direct_interrupt`

这也是项目里“人类在环侧观察、偶尔高优先级介入”真正落成技术方案的关键。

### 5. Ecosystem strategy

EvoMap / MCP / A2A / OpenClaw 这类外部生态，应被放到两个层级中理解：

1. `tooling / protocol ecosystem`
   - 帮助 Freely 接入外部能力、复用经验、交换资产
2. `runtime leverage`
   - 在某些阶段借现成 runtime 落地 Freely 能力

但它们都不应替代：

- Freely 的治理规则
- Freely 的状态词典
- Freely 的边界 contract

## 四、控制面 UI 的进一步收敛

### 1. Chat 是入口，但不能成为唯一主视图

用户会和 AI 对话，这是控制面的一部分，但如果整个产品只剩 chat：

- 无法同时观察多个 run / agent / worktree
- 很难理解系统当前是在正常推进、等待、阻塞还是恢复
- 团队态势会被淹没在线性消息流中

因此更稳的判断是：

- `chat intervention panel` 是高优先级输入入口
- 但不是整个应用的信息架构中心

### 2. Terminal 应是可附着工作面，而不是唯一世界

终端在 Freely 里依然关键，因为：

- AI CLI 真正在 PTY 中执行
- 错误、流式输出、命令细节、调试都需要终端面

但它更适合被定义成：

- `embedded terminal`
- 可按 session / run / agent attach
- 与 team timeline、agent roster、status panels 并列

而不是“应用本体 = 一个终端窗口”。

### 3. 多 worktree / 多 agent / 多 subagent 观察应成为一级布局对象

Freely 的产品目标天然要求系统能并行观察多个执行单元，因此布局上至少要支持：

- `project switcher`
- `worktree lane` 或 `workspace lane`
- `agent roster`
- `run / stage summary`
- `team timeline`
- `terminal attachment surface`
- `chat intervention panel`

这里需要再补一句边界：

- `worktree`、`session`、`run` 是 Freely 当前应显式治理的一等对象
- `subagent` 当前更接近 AI 在提示词和工具能力下的内部执行安排
- 控制面可以展示 subagent 结果或活动痕迹，但不要求 day-1 backend 先把每个 subagent 做成强实体

一个更接近产品语义的心智模型不是“IDE 标签页”，而是：

- 左侧：项目 / worktree / session 导航
- 中央：团队时间线 + 关键状态卡片
- 右侧：当前选中 agent / run 的细节与控制
- 底部或可切换区域：附着式终端

### 4. 布局需要大胆，不应被传统 IDE 绑住

Freely 的核心任务不是手写代码编辑，而是：

- 观察自治团队
- 纠偏
- 打断
- 恢复
- 在多个 worktree / 多个 AI 之间切换判断

因此 UI 可以更接近：

- control room
- mission operations board
- AI team dispatch surface

而不是“代码编辑器 + 聊天侧栏”的保守拼装。

### 5. Day-1 也应保留这种方向，而不只是临时凑一个 probe

即使 day-1 只做 `Frontend Probe`，也不应把 Probe 降格成：

- 单列消息流
- 单 terminal 输出
- 看不到 worktree / agent / 阶段状态的最小 demo

更合理的 day-1 Probe 是“薄，但方向正确”：

- 能看 project
- 能看多个 run / agent
- 能附着终端
- 能发 chat intervention
- 能看 stage / blocker / recovery

## 五、Skill-first 生态暴露的进一步收敛

### 1. Freely 的能力最好先在自己内部以 skill 暴露

如果 Freely 把自己的主要能力都先收敛成 skills：

- discovery / routing
- pre-brainstorm
- IBM
- dev-loop
- recovery
- governance

那么它会天然获得三件事：

- 内部执行边界更清晰
- UI 与 backend 更容易围绕能力构建
- 对第三方生态更容易投影和适配

### 2. OpenClaw 的 workspace 可扩展面，适合做能力投影层

OpenClaw 目前最有价值的不是替代 Freely 的产品，而是：

- workspace 自定义
- skills 覆盖
- memory / session 连续性
- hooks / cron 等工作区能力

因此更合理的关系是：

- Freely 自己先定义能力语义
- OpenClaw workspace 用来承载其中一部分能力投影
- 由 adapter / profile 做映射，而不是让 Freely 本体反向依赖 OpenClaw 的内部结构

### 3. “skill-first” 还能降低第三方集成的污染半径

如果没有 skill 边界，第三方接入很容易直接碰：

- 后端状态机
- UI 特殊逻辑
- 项目治理细则

如果先经过 skill 和 contract 层，第三方更可能只接触：

- 能力入口
- 输入输出约束
- 可审计事件

这比直接暴露内部实现更稳。

## 六、独立于 OpenClaw 的技术运行基线

### 1. 仓库里其实已经有一条 standalone runtime 骨架

从现有脚本和 skills 看，Freely 并不是“还没对接 OpenClaw 就什么都没有”，而是已经具备一个最小独立运行骨架：

- `docs/system/workspace/scripts/runtime/freely`
  - 提供 `init/doctor/start/status/stop`
  - 管理项目内 `.freely/` 状态目录
  - 持有 supervisor 循环与重启语义
- `docs/system/workspace/scripts/start-lead-agent.sh`
  - 负责组装首跳提示，进入 `lead-agent -> context-source-skill`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
  - 负责启动和监控外部 AI CLI
  - 已支持 `codex`、`iflow`、`kiro-cli`
- `docs/system/workspace/skills/**`
  - 作为治理、路由、文档环、开发环、恢复环的执行真源

这说明：

- Freely 当前已经具备“无 OpenClaw”独立运行骨架
- 它依赖的是外部 AI CLI，不依赖某个固定 agent runtime 框架

但也要明确当前未闭合点：

- 首跳依赖如 `docs/milestones.md` 还未被 `doctor/start` 完整门禁化
- standalone contract 仍需被正式冻结
- “可独立运行”当前更接近架构方向和最小骨架，而不是完全闭合的产品交付态

### 2. 无 OpenClaw 时，Freely 的最小运行面是什么

如果不接 OpenClaw，Freely 仍然可以靠以下技术面成立：

1. `project governance input`
   - `PROJECT_INTENT`
   - `CONSTITUTION`
   - `LAWS`
   - `AGENTS`
2. `runtime supervisor`
   - `freely start/status/stop`
   - `.freely/run/*.pid`
   - `.freely/logs/*`
3. `AI execution adapter`
   - `codex`
   - `iflow`
   - `kiro-cli`
4. `skill execution truth`
   - `context-source-skill`
   - `doc-pre-brainstorm-execution`
   - `doc-ibm-execution`
   - `dev-loop-execution`
   - `recovery-subagent-governance`
5. `workspace governance`
   - worktree rules
   - hooks
   - governance-check
6. `state evidence`
   - milestones / issues / progress / recovery
   - prompt files
   - pid / log files
   - session refs

研究优先阶段补充：

- 若 `docs/progress/**` / `docs/recovery/**` 尚未完全启用，当前仍允许 `docs/B1-docs/raw-CONVERGENCE.md` 作为等价证据落点

### 3. 无 OpenClaw 时，memory 不能消失，只是实现形态不同

如果没有 OpenClaw 的 memory/session 能力，Freely 仍需自己承接最小连续性：

- 当前项目状态
- 当前 branch / worktree
- 当前 issue / phase
- 当前 tool / session_id
- 当前 prompt 和最近一次运行日志
- 当前恢复定位线索

按现有设计，这些连续性至少可由以下事实组合承担：

- `docs/milestones.md`
- `docs/epics/**`
- `docs/progress/**` / `docs/recovery/**`
- `.freely/logs/*`
- `.freely/run/*`
- `session_refs`

也就是说：

- OpenClaw memory 是增强项
- Freely 自身的文档状态 + runtime state + session evidence 才是基础兜底层

### 4. 无 OpenClaw 时，skills 不是替代品，而是主能力面

如果没有 OpenClaw，Freely 的 skills 并不会失效，反而会更明确地成为主能力接口：

- skills 决定 How
- runtime 脚本负责托管和监控
- 外部 AI CLI 负责具体执行

因此 standalone 方案的核心关系是：

```text
Freely governance + skills
  -> Freely runtime supervisor
  -> external AI CLI via PTY
  -> project artifacts and evidence
```

这条链已经足够表达一个独立产品最小闭环。

### 5. OpenClaw 集成应被理解为增强模式，而不是基本模式

在这个基础上，OpenClaw 能提供的价值应被严格定义为增强：

- 更强的 memory / session 连续性
- workspace 级扩展与 skill 覆盖
- hooks / cron / agent profile 生态

但如果这些增强缺席，Freely 仍应维持：

- 自治主链
- 规则治理
- worktree 执行
- 恢复与重启
- UI 控制面

### 6. 技术上应该明确区分两种运行模式

后续更稳的架构表述可以直接分成两种 mode：

1. `standalone mode`
   - Freely runtime + Freely skills + external AI CLI
   - 不依赖 OpenClaw
2. `integrated mode`
   - Freely contract / skills / governance
   - 加上 OpenClaw workspace/profile/memory 作为增强 adapter

这样就能避免未来所有技术讨论都被“要不要接 OpenClaw”绑架。

## 七、技术栈分层草案

### 1. Frontend stack

- `Tauri`
  - 桌面应用容器
- `React`
  - 控制面 UI
- `TypeScript`
  - 前端类型边界
- `Bun`
  - 前端包管理 / 脚本运行时
- `xterm.js`
  - embedded terminal 渲染

不应进入 frontend runtime 本体的内容：

- OpenClaw SDK/runtime 语义
- AI CLI 工具本体
- Rust backend 内部治理逻辑

### 2. Backend stack

- `Rust`
  - backend service core
- `Rust PTY`
  - 终端进程与 attach
- `Tauri backend`
  - day-1 transport bridge

后端负责：

- session/run/governance/recovery 事实状态
- tool adapter
- event / snapshot
- input arbitration

### 3. Execution tool stack

- `codex`
- `iflow`
- `kiro-cli`

它们不是产品技术栈本体，而是：

- AI execution adapters
- 可替换执行资源
- 受 Freely runtime 与 skills 调度

### 4. Integration / ecosystem stack

- `OpenClaw workspace/profile`
- 未来 `ws_adapter`
- 未来其他 runtime/profile

这层不应反向定义产品内核。

### 5. Manifest / truth-source layering

后续实现时建议明确：

- frontend truth source
  - `package.json`
  - `bun.lock`
- backend truth source
  - `Cargo.toml`
  - `Cargo.lock`
- governance truth source
  - `PROJECT_INTENT`
  - `CONSTITUTION`
  - `LAWS`
  - `AGENTS`
- execution tool truth source
  - `docs/system/workspace/tools.md`
  - 后续独立 capability doc/json

## 八、这次梳理后最值得推进的问题

### 1. 应先冻结“backend service contract”，而不是直接扩写 transport API

否则会继续在 HTTP / WS / Tauri invoke 之间摇摆，难以形成真正稳定的中间层。

### 2. 应把“adapter taxonomy” 文档化

现在大家已经口头接受 `tauri_adapter`、`ws_adapter`，但还没有统一说明：

- 哪些 adapter 是产品内建
- 哪些 adapter 是生态集成
- 哪些 adapter 只是研究占位
- 每类 adapter 应遵守什么兼容约束

### 3. 应把“前端 manifest / 后端 manifest / agent tooling capability” 三者分开

否则后面很容易把产品依赖、开发依赖、agent 外部工具能力混写。

### 4. 应重新定义“Freely 是否依赖 OpenClaw”

更准确的表述应是：

- Freely 产品不依赖 OpenClaw 才能成立
- 但可以拥有一个 OpenClaw adapter/profile 作为阶段性实现路径

### 5. 应把 standalone runtime baseline 单独冻结

否则“Freely 自己到底靠什么独立运行”会一直隐含在脚本和 skill 里，难以成为产品架构的明确承诺。

### 6. 应把 human intervention transport 单独冻结

否则 `chat intervention panel`、`SendChatIntervention`、`session_id/resume_hint`、以及各家 CLI 的 resume/attach 差异会继续分散在 UI、恢复和工具接入讨论里，难以形成稳定控制链。

## 九、当前更清晰的产品表述

建议用下面这句话统一口径：

> Freely 是一个以 Rust 后端控制面为事实核心、以 Tauri + React 作为跨平台客户端壳、以稳定 command/event/snapshot contract 解耦 transport 与 runtime、以 AI 团队控制面而非单终端为产品体验、并可通过 skill 与 adapter 对接外部 AI CLI 与第三方 runtime 的自治软件工程系统。

这句话比“一个 CLI 编排器”或“一个桌面应用”都更完整。

## 十、推荐下一跳

1. 先补一个正式的“Backend Service Contract / Adapter Taxonomy” issue
2. 再补一个“技术栈分层与 manifest 真源” issue
3. 再补一个“AI Team Control Surface / Multi-Worktree Visibility” issue
4. 再补一个“Skill-first Capability Exposure and OpenClaw Workspace Projection” issue
5. 再补一个“Standalone Runtime Baseline Without OpenClaw” issue
6. 再补一个“Human Intervention Transport Across Auto-Run CLIs” issue
7. OpenClaw 相关内容保留为 adapter/profile 方向，不把它抬成主架构
8. Frontend Probe 继续作为 day-1 验证面推进，但其依赖对象应改为已冻结 contract，而不是漂浮 API 草案
