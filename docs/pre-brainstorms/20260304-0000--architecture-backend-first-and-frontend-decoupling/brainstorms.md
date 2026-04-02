# 研究：Freely 的后端优先与前后端解耦路线

## 背景

基于当前讨论，Freely 的产品形态应明确为：

- 前端：自有 App（交互体验可参考 Codex App）
- 后端：具备 CLI 执行环境的 Agent Runtime（可本地，可远端）
- 持久化：记忆与会话（jsonl/结构化状态）可跨设备续接

本研究聚焦：先做什么、怎么解耦、OpenClaw 与自建后端如何取舍。

---

## 核心结论

1. **前后端分离是硬约束**。  
   前端不直接读写 workspace 文件，不直接耦合具体 runtime。

2. **先后端、后前端** 是当前最优路径。  
   先把 workspace + 会话/记忆 + CLI 编排跑通，再做 UI。

3. **状态层必须可跨设备**。  
   代码仓库（Git）用于代码与文档同步，不适合作为高频会话状态主存储。

4. **短期建议采用 OpenClaw Runtime + 自有 API 适配层**。  
   快速落地、风险更低；同时保留后续替换 runtime 的空间。

5. **前端与 OpenClaw 的交互主链路使用 Gateway API（WS/HTTPS），不以 channel 模式作为主路径**。  
   channel 更适合 Telegram/飞书等外部消息面；自有前端应作为控制面客户端接入。

6. **需求发现主链路从 `chat sessions -> pre-brainstorms -> issue` 演进**。  
   早期不强制 epic/story 命名，先吸收不确定输入，再在后续环节规范化。

---

## 为什么先不做前端

当前主要不确定性不在 UI，而在后端闭环能力：

- 会话连续性是否稳定（恢复、切换设备、并发访问）
- 记忆读写与检索是否可靠
- CLI 编排是否可控（超时、错误、重试、日志）
- 工程治理是否可执行（门禁、流程、审计）

若这些未稳定，前端先行会导致高返工。

---

## Freely 循环模型（本次补充）

Freely 的执行思想补充为三层循环：

1. `auto-loop`：自治调度与持续推进（发现需求、触发执行、异常恢复）
2. `doc-loop`：文档约束下的规范化沉淀（研究、规划、映射）
3. `dev-loop`：按文档执行实现与验证（可多 AI CLI 协作）

### 人类在 loop 中的角色

- 默认为旁观与信息注入，不阻塞循环
- 人类对话是 side-channel（用于疑问、澄清、补充）
- 仅在显式停止/阻塞指令下暂停 loop

---

## 研究能力与前置产物组织

Freely 自身需要“研究能力”，因此在 `docs/` 下新增前置研究层：

主流程：

`chat sessions -> pre-brainstorms -> issue`

含义：

- `chat sessions`：原始讨论事实源（jsonl/session）
- `pre-brainstorms`：前置研究收敛层（可选输入吸收器）
- `issue`：正式进入执行与规划体系的需求项

### pre-brainstorms 目录组织（自包含，最小化）

采用“一个 pre-brainstorm 一个目录、两份核心文件”：

```text
docs/pre-brainstorms/
  INDEX.md
  <pre-brainstorm-name>/
    brainstorms.md
    candidates.md
```

约束：

- `brainstorms.md`：记录本次研究/讨论过程（可多轮）
- `candidates.md`：唯一候选产出文档，集中记录 0~N 个候选 issue
- 避免过多子目录与碎片文件

`<pre-brainstorm-name>` 建议格式：

`YYYYMMDD-HHMMSS--<source>--<topic>`

---

## 候选产物到 Issue 的收敛规则

`candidates.md` 中每个候选项建议包含：

- `candidate_id`
- `title`
- `problem`
- `why_now`
- `acceptance_hint`
- `priority`
- `status`（`proposed | promoted | dropped`）
- `promoted_issue_path`（可空）
- `session_refs`（jsonl 或 session id）

说明：

- `pre-brainstorms` 的结束产物是候选 issue 集
- 可一次产出一个或多个 issue
- 后续由 `doc-loop`/`planning` 决定如何映射到 epic/story/milestone

---

## Skills 插槽化演进（本次补充）

Freely 的方法论与执行策略应通过 skills 插槽持续升级，而非硬编码在主流程：

- `discovery` 插槽：多来源需求发现
- `pre-brainstorm synthesis` 插槽：前置研究收敛
- `planning` 插槽：issue 到 epic/story/里程碑映射
- `dev orchestration` 插槽：多 CLI/多 agent 协作验证
- `recovery` 插槽：崩溃重启与会话接续策略

这样可在不改主循环骨架的前提下，迭代“怎么做”的策略。

### Skills 目录分层（最小约定）

为兼顾内置能力与用户自定义，skills 采用双工作区：

- `system/workspace/skills/`：Freely 内置技能（随版本发布）
- `user/workspace/skills/`：用户技能（项目自定义）

后续资源（如 `prompts/`、`templates/`）可并列在各自 workspace 下扩展，不混入 `skills/` 根。

### Skills 解析优先级（按你方当前决策）

1. 默认开启“用户同名接管”。
2. 若 `user/workspace/skills/` 存在同名 skill，则优先使用用户 skill。
3. 若不存在同名 skill，回退到 `system/workspace/skills/`。
4. 若用户手动关闭该 skill 的接管开关，则强制回退系统 skill。

这条规则的语义是：用户创建同名 skill，默认就是希望接管该职责。

### Skills 强制执行点（避免仅靠提示词）

需要在后端运行时增加统一门禁：

1. skill 执行时注入不可伪造上下文（`skill_id`、`skill_run_id`、`mode`、`workspace_source`）。
2. 所有文件写入经过统一 write gateway，而非直接写文件。
3. gateway 基于路径策略校验：
   - `docs/**` 仅允许文档相关 skill（如 `doc-writer`）写入。
4. 写入审计事件必须落盘，支持追溯与恢复。
5. 非法写入（无 skill 上下文/上下文不匹配）立即拒绝并回报错误事件。

这定义了“必须经过”的技术落点：是 runtime enforcement，不是 skill 文案建议。

### 每个 Skill 的 UI 控制面（避免过度设计）

在 skill 列表中，每个 skill 仅保留三类模式滑块：

1. `接管`：使用同名用户 skill 全流程执行。
2. `微调`：系统 skill 主流程执行，调用用户逻辑作为补充步骤。
3. `附言`：在系统 skill 结果末尾拼接用户自然语言指令片段。

并为每个 skill 显示：
- 启用/关闭开关
- 当前模式滑块
- 职责小字说明（只描述职责，不暴露内部控制细节）
- 来源标签（`system/workspace` 或 `user/workspace`）

---

## 目标架构（解耦形态）

三层结构：

1. `Frontend`：你的 App（Web/Desktop/Mobile）
2. `Backend API`：统一协议层（你定义）
3. `Runtime`：OpenClaw 或自建执行内核（可替换）

原则：

- 前端只依赖 Backend API，不感知 runtime 细节。
- runtime 只处理执行与状态，不承担产品 UI 逻辑。
- 状态存储独立于前端，支持跨设备访问与恢复。

该解耦的直接收益：

- 可从 OpenClaw 平滑迁移到自研 runtime 或其他 `xxclaw` 变体
- 前端无需因后端替换而重写，只需保持 Backend API 兼容
- 运行时能力可按阶段替换（先借力，后自主）

---

## 后端部署模式

### 模式 A：本地后端

- 优点：延迟低、调试快
- 缺点：跨设备弱、续接体验差
- 适用：单机开发与调试阶段

### 模式 B：远端后端（推荐主模式）

- 优点：可跨设备续接、状态集中、协作更稳定
- 缺点：需要运维与网络环境
- 适用：产品化与长期运行

建议：本地仅作开发调试，生产/长期运行以远端后端为主。

---

## OpenClaw vs 自建后端

### 采用 OpenClaw 的收益

- 已有能力完整：会话、记忆、hooks、cron、多渠道、工具编排
- 基础设施成本低：减少大量平台工程工作
- 迭代更快：把资源集中在 Freely 方法论与产品体验

### 采用 OpenClaw 的约束

- 运行模型与配置模型需遵循其框架
- 某些 Freely 语义（如强 supervisor 模式）不完全原生
- 需要 API 适配层降低平台耦合

### 自建后端的收益

- 语义完全可控（会话/记忆/恢复策略）
- 数据模型可长期稳定自定义

### 自建后端的成本

- 平台工程工作量显著增大（PTY、调度、并发、权限、安全、运维）
- 早期验证速度下降

**决策建议**：

- 短期：OpenClaw Runtime + 自有 Backend API 层
- 中期：固化自有状态模型与接口协议
- 长期：若受限再渐进替换 runtime

---

## 前端未来对接方式（协议草案）

前端只对接 Backend API，最小接口集合建议：

1. `POST /sessions`：创建/恢复会话
2. `GET /sessions`：会话列表
3. `POST /sessions/{id}/messages`：发送消息
4. `GET /sessions/{id}/stream`：流式输出（SSE/WebSocket）
5. `GET /sessions/{id}/history`：会话历史（jsonl 聚合视图）
6. `GET /memory/search?q=...`：记忆检索
7. `POST /commands/run`：受控命令执行（可选）
8. `GET /status`：后端健康状态

---

## Chat 与 Sessions 设计（本次补充）

### 基本抽象

- `chat`：人类输入通道（交互入口）
- `sessions`：执行与事实时间线（jsonl 持久化）

解释：

- chat 是“输入”
- session 是“状态与事件事实”
- 前端输入框只负责发输入事件，chat list 展示 session 时间线

### UI 职责拆分（先抽象，不绑定具体样式）

1. 输入框（Human Input）
   - 人类发送指令、澄清、纠偏
2. Chat List（Session Timeline）
   - 显示混合事件：人类消息 + AI 自治执行事件
   - 人类可旁观 AI 自治过程（例如 pre-brainstorms/brainstorms/dev-loop 事件）

补充交互：

- chat list 中任一会话可展开会话输入框
- 该输入框仅作用于当前会话，用于澄清与干预

### 干预模型（支持运行中语义干预）

建议支持三类输入：

1. `normal_message`
   - 常规消息，按会话顺序处理
2. `soft_interrupt`
   - 语义纠偏（如“这不对，重新思考”）
   - 高优先级注入当前会话语境
3. `hard_interrupt`
   - 强中断（如“停下”）
   - 立即终止当前执行并进入新指令

说明：

- 会话执行保持串行，避免并发乱序
- 中断行为应写入 session jsonl，保证可追溯

### 建议事件类型（session jsonl）

- `human_message`
- `ai_message`
- `loop_started`
- `loop_finished`
- `pre_brainstorm_created`
- `candidate_issues_updated`
- `issue_promoted`
- `dev_run_started`
- `dev_run_finished`
- `recovery_triggered`
- `interrupted_by_human`

### 与 OpenClaw 的具体交互建议

主路径：

- 前端（或 BFF）直接连接 OpenClaw Gateway 的 WS/HTTPS 接口
- 以会话/agent RPC 为中心（`agent`、`agent.wait`、`sessions_*`、`cron_*`）
- 前端自己渲染流式输出与会话视图

不作为主路径：

- 不把自有前端优先建成 OpenClaw channel 插件

何时考虑 channel/插件：

- 仅在需要“把你的产品当作外部消息渠道”接入时（类似 Telegram/飞书）再做

这确保：

- 前端可独立演进
- runtime 可替换
- 会话与记忆可迁移

---

## 多项目 UI 隔离规范（新增）

目标：在同一工作区同时观察多个项目时，仍保持清晰的人机操作边界与项目隔离语义。

### 核心原则

1. 右侧交互区始终存在 `activeProjectId` 语义。
2. 左侧项目树选中态是唯一主锚点，驱动右侧高亮与默认发送目标。
3. 多项目并行展示时，每个项目仍保留独立 chat 上下文与输入草稿。

### UI 模式

建议提供顶部模式开关：

1. `Focus`（单项目模式）
   - 右侧仅展示 `activeProjectId` 对应项目的 chat 区。
2. `Overview`（多项目模式）
   - 右侧同时展示多个项目 chat 卡片。
   - 左侧当前选中项目在右侧对应卡片高亮显示。

### 交互规则

1. 左侧点击项目 A：
   - 更新 `activeProjectId = A`
   - Focus 下切换右侧到 A
   - Overview 下仅切换高亮目标到 A
2. 发送消息：
   - 默认发送到 `activeProjectId`
   - 若在某项目卡片内触发发送，则发送到该卡片项目
3. 启动自治开发：
   - 必须绑定触发来源项目 `projectId`
   - 后端按该 `projectId` 绑定 `cwd/sandbox/memory namespace`
4. 切换左侧选中项目不应中断其他项目已有运行

### 项目级独立状态（必须）

每个项目至少独立维护：

- `chat list`（会话时间线）
- `input draft`（输入框草稿）
- `agent status`（idle/running/error）
- `run metadata`（runId、开始时间、最近事件）

### 推荐状态模型（TypeScript）

```ts
type UiMode = "focus" | "overview";

interface WorkspaceState {
  uiMode: UiMode;
  activeProjectId: string;
  projectOrder: string[];
  chatSessionByProjectId: Record<string, string>;
  draftByProjectId: Record<string, string>;
  agentRunByProjectId: Record<
    string,
    { status: "idle" | "running" | "error"; runId?: string }
  >;
}
```

### 防误操作约束

1. 右侧顶部持续显示当前高亮项目（名称 + 绝对路径）。
2. 发送前校验：请求体中的 `project_id` 与目标项目一致。
3. 事件流按 `project_id` 分发，前端按项目订阅并渲染，避免跨项目消息串线。

---

## 当前阶段执行建议

1. 先完成 backend/workspace 闭环，不启动前端开发
2. 抽象并冻结第一版 Backend API 协议
3. 在 OpenClaw 上实现 Freely 的 workspace 画像（AGENTS/skills/hooks/cron）
4. 以远端后端模式作为主运行路径
5. 前端待后端协议稳定后再接入

补充执行决策：

- 先按“Gateway API 直连/BFF 转发”方案推进
- 将 channel 插件路线降级为后续可选扩展

---

## 与既有研究关系

本研究承接以下结论：

- [20260304-0000--openclaw-workspace-freely-feasibility.md](./20260304-0000--openclaw-workspace-freely-feasibility.md)

即：在不改 OpenClaw 源码前提下，可通过配置+workspace 方式承载 Freely 的主要能力；本篇进一步将其产品化路线明确为“后端优先、前后端解耦、前端后置接入”。
