# 研究重做：面向“AI 自主当主人”的 Freely 对齐分析

## 0. 研究目标（重置）

本次只以两份一手约束为准：
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`

目标不是“再找一个新概念”，而是回答：
1. Freely 到底是什么系统？
2. 现有研究哪些地方偏离了这个系统身份？
3. 下一步该产出什么，才能把工具做成“开发时 AI 自己当主人”？

---

## 1. 项目身份（最终判定）

Freely 的产品身份已经足够清晰：

1. **不是任务执行器**，而是“AI 担任项目 owner 的自主工程循环系统”。
2. **核心不是接某个协议**，而是把“发现 Issue -> 文档 -> 开发 -> 验收 -> 恢复 -> 下一轮”跑成持续闭环。
3. **宪法是硬约束，不是建议**：分支/工作树、恢复策略、技术栈、方法论、并行委托都必须落实到可执行门禁。
4. **最小输入面固定**：项目路径、意图路径、宪法路径、AI 规格；其余上下文由 AI 自主发现。

这意味着：Freely 的第一优先级是“owner 治理能力产品化”，不是“生态接入能力最大化”。

---

## 2. 现有研究复盘（按对齐度）

### A. `20260303-0000--ai-consistency-closed-loop-freely-alignment.md`

可保留：
- Ring/SSOT/自包含/测试围栏/独立监理这些机制，与意图+宪法高度兼容。
- 把“方法论”翻译成“Skill + Gate”的方向正确。

需修正：
- 外部文章是社区讨论整理，不是正式规范；可作启发，不可直接当硬标准。
- 应明确：Freely 的硬标准来源仍是本项目宪法和文档法（LAWS），外部文章仅作设计输入。

### B. `20260303-0000--cli-orchestration-architecture.md`

可保留：
- CLI 编排、会话恢复、验收先行这些方向正确。

需修正：
- “品味.md”作为中心约束文件容易弱化宪法权威，应该改为“宪法+项目意图+规范文档”的分层输入。
- 将外部工具当“主要执行体”存在风险：Freely 需要先有自有的治理内核，再决定工具接入边界。

### C. `20260304-0000--evolver-integration.md` 与 `20260304-0000--evomap-ecosystem-freely.md`

结论：**方向可研究，但当前阶段优先级过高且部分事实已过时/不严谨。**

核验后发现：
1. 研究文档中 A2A 报文示例字段使用了 `version/type` 等写法；官方文档当前为 `protocol_version/message_type/message_id`（存在格式漂移风险）。
2. 任务接口是 REST JSON，不走完整 A2A envelope，旧文档未强调这一关键差异。
3. “Freely 升级为进化系统”本身并不违背愿景，但会挤占 owner 闭环核心建设资源，容易本末倒置。

判定：
- EvoMap 可作为**后续可选能力源**，不应成为当前架构主轴。

---

## 3. 外部链接再核验（本次重查）

### 3.1 `https://www.wanghuan.ai/blog/ai-consistency-closed-loop`

- 该链接直接访问返回 SPA 外壳，正文需从前端 bundle 获取。
- 可确认文章核心主张：Ring 分层、SSOT、自包含文档、测试围栏、独立监理、前置纠偏。
- 这些观点与 Freely 目标兼容，但来源属性是“社区经验总结”，不是强制规范。

### 3.2 EvoMap 官方资料（`evomap.ai`）

已对照：
- `docs/en/03-for-ai-agents.md`
- `docs/en/05-a2a-protocol.md`
- `api/docs/wiki-full`
- `a2a/skill?topic=task|publish`

可确认：
1. 协议细节较多且仍在演进，接入成本不低。
2. A2A 发布要求 Gene+Capsule bundle（`payload.assets`），并有具体门槛与限流规则。
3. 任务体系（claim/complete/submit/list）是独立 REST 端点，不等同于 A2A 协议消息封装。

---

## 4. 面向“自己当主人”的产品化输出（应产出什么）

Freely 应优先产出的是“Owner 内核”，不是“外部能力市场适配层”。

### 4.1 必须先落地的 8 个内核能力（P0）

1. **Issue Discovery Engine**
- 从意图、进度、review、test、chat 输入/会话证据、GitHub issue 汇聚候选 Issue。

2. **Issue Router**
- 按宪法规则路由到 `doc-loop(IBM+G)` 或 `dev-loop(DDD)`。

3. **Governance Gate Engine**
- 分支/工作树规则、PRE_TEST、review 记录、可追溯性检查自动门禁。

4. **Owner State Machine**
- “发现 -> 规划 -> 实施 -> 验收 -> 归档 -> 下一轮”的显式状态机。

5. **Recovery Controller**
- 续接优先，无法续接时桥接恢复；写入 progress/recovery 后自动重启循环。

6. **Sub-agent Batch Orchestrator**
- 按宪法 12/13 章进行并行委托、批次等待、失败回退、审计记录。

7. **Doc Contract Compiler**
- 将 Story 验收条件编译成可执行检查项（至少先覆盖集成测试门禁）。

8. **Promotion & Cleanup Enforcer**
- `feature -> pre-develop -> develop` 提升链、合并后分支/工作树清理强制执行。

### 4.2 可后置的扩展能力（P1/P2）

- P1：外部工具适配层（Claude/OpenCode/其他 CLI）统一封装，但仍受 Gate Engine 控制。
- P2：EvoMap/A2A 适配作为插件化能力，默认关闭，仅在不破坏主闭环时启用。

---

## 5. 本次重做后的总判断

1. 之前研究最大问题不是“技术点错”，而是**主次错位**：把生态接入讲得比 owner 内核还重。
2. 对 Freely 来说，最关键的不是“AI 能不能调用更多外部能力”，而是“AI 是否被制度化为可审计、可恢复、可持续的项目 owner”。
3. 下一阶段研究/开发应该围绕“内核 8 能力 + 强制门禁”展开；外部生态只做可插拔增益，不做主流程依赖。

---

## 6. 建议立即落文档的三个规范（短期）

1. `Owner Loop Contract`（定义状态机与每步输入/输出）
2. `Gate Contract`（定义必须通过的门禁与失败处理）
3. `Recovery Contract`（定义续接/桥接触发条件与文档写回格式）

只要这三份契约先落地，Freely 才真正开始从“想法”走向“主人式自动工程系统”。

---

## 7. 本轮补充结论：Skills-First 闭环落地

### 7.1 总原则（确定）

1. 所有 loop 的执行指导通过 `skills` 落地，不把流程细节硬编码在主循环。
2. loop 之间是“契约解耦”，不是“彼此无关”：
   - 彼此不依赖内部实现
   - 通过标准输入/输出契约闭环协作
3. 文档规则必须自包含于文档相关 skills，其他 loop 通过调用文档 skill 落盘，不直接散写文档。

这条原则的直接收益：
- 升级流程时只需替换/升级 skills，而不需要重写主循环骨架。

### 7.2 三个 loop 的职责边界（当前共识）

1. `A:auto-loop(ADD)`：发现、路由、调度、恢复触发。
2. `D:doc-loop(IBM+G)`：文档结构化产出与约束沉淀（issue/prd/pre-tests/tasks/里程碑/进度 + 治理一致性修复）。
3. `D:dev-loop(DDD)`：读取文档约束执行开发并回传结果，不负责定义文档写法。

### 7.3 D:dev-loop(DDD) 的最小执行骨架（工作草案）

`Read Doc -> DevDev -> Update Doc`

其中 `Read Doc` 必须先完成，至少读取：
- 里程碑（决定当前应处理的 epic/story/issue）
- 进度目录（识别 in-progress/blocked）
- IBM 产物：`issue`、`prd`、`pre-tests`、`tasks`
- 对应 dev-loop skills 指南

建议目标产物路径（重构后）：

`epics/{epic-name}/{story-name}/[issues/{issue-name}.md, prd.md, pre-tests.md, tasks.md]`

并与里程碑、进度目录形成闭环映射。

### 7.4 文档写入策略（必须）

1. 文档写入由 doc skills 统一执行（可称 `doc-writer` 能力）。
2. auto/dev loop 只提交结构化结果载荷，不直接决定文档格式细节。
3. 所有写入操作必须可追溯（写入来源 loop、输入契约、时间戳）。

### 7.5 Skills 覆盖策略（本轮定稿）

为满足“可自定义但不过度设计”，采用最小覆盖模型：

1. 双工作区目录：
   - `system/workspace/skills/`
   - `user/workspace/skills/`
2. 同名即接管（默认开启）：
   - 若用户目录存在同名 skill，默认由用户 skill 接管。
   - 若用户手动关闭该 skill 接管，则回退系统 skill。
3. 每个 skill 三种模式：
   - `接管`：用户 skill 全流程执行
   - `微调`：系统 skill 主流程 + 用户逻辑补充
   - `附言`：系统 skill 结果末尾拼接用户自然语言指令
4. 列表展示最小信息：
   - skill 名称
   - 职责小字说明（不泄露内部控制细节）
   - 来源（system/user）
   - 开关与模式

该策略保证：
- 用户“想自定义就生效”
- 系统实现仍保持可控、可调试、可回退

### 7.6 强制机制与 Skills 的分工（本轮定稿）

为避免“只靠提示词约束”失效，必须区分两层：

1. **Enforcement（架构强制层）**
   - 负责“必须经过某 skill 才能做某事”。
   - 例如：写入 `docs/**` 只能通过 `doc-writer` 路径，其他直接写入一律拒绝。
2. **Skill Policy（策略层）**
   - 负责“经过后怎么做才正确”。
   - 例如：`doc-writer` 内执行 SSOT、自包含、验收字段与冲突修复规则。

结论：
- `必须经过` 不属于文案约束，而是运行时门禁约束。
- `怎么写好` 由 skills 持续演进。

### 7.7 如何判定“是否通过某个 Skill”

采用“执行上下文标记 + 写入网关校验”：

1. skill 运行时由 runtime 注入上下文：
   - `skill_id`
   - `skill_run_id`
   - `mode`（接管/微调/附言）
   - `workspace_source`（system/user）
2. 所有文件写入必须经过统一 write gateway。
3. gateway 按路径策略校验上下文权限（如 `docs/**` 仅允许 `doc-writer`）。
4. 每次写入落审计事件（谁在何时以哪个 skill run 写了哪些文件）。
5. 无上下文或上下文不匹配时直接拒绝写入。

### 7.8 防遗忘引用

关于技能设计中的统一理念速记（宪法/法律、Ring、SSOT、自包含、验收先行、集成优先、自治闭环、enforcement vs policy），统一维护在：

- `docs/research/README.md` 的“Skills 设计速记清单（防遗忘）”。
