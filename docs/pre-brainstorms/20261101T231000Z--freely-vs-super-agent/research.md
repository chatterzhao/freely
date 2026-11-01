---
pre_brainstorm_id: PB-20261101T231000Z
phase_state: in_progress
topic: Freely vs DeepSeek Super-agent
sources:
  - DeepSeek Harness article (2026-10-31)，经智东西/博客园两篇按原文结构复述的报道交叉核对
  - deepseek-ai/dsh-superagent-prototype（2026-11-01 main 快照）
  - Freely docs/PROJECT_INTENT.md、CONSTITUTION.md、LAWS.md
  - Freely docs/system/workspace/three-loop-capability-lifecycle.md、ibm-framework.md、scan-lifecycle-design.md
  - Freely docs/system/workspace/a2a/*、agents/*、tools.md、commands.md、acp-session-architecture.md
  - Freely runtime/scripts/gates 关键实现
created_at: 2026-11-01
---

# 预头脑风暴：Freely 与 DeepSeek Super-agent 到底在解决什么问题

> 这不是“功能清单对比”，也不是给 Freely 找背书。它要回答的是：两个系统各自把什么当作第一性问题、用什么机制解、在哪个问题上更优、代价是什么。研究没走完之前，不 promote、不写实现。
>
> 本文取代 `docs/B1-docs/raw-20261101T031502Z/brainstorms.md` 的对比框架；B1 文档保留 P0 `harness-status` 的实现记录与任务拆分，但凡涉及“Freely 是什么、谁更优”的判断，以本文为准。

## 0. 要回答的五个问题

1. 两个系统在上层理念上有什么共同点？这些共同点是不是同一个问题的不同答案？
2. Freely 的真实架构是什么？文档、runtime、script、skill、command、MCP、agent harness 各自处在哪一层、谁驱动谁？
3. Super-agent 的真实架构是什么？文章主张与原型实现差在哪？
4. 在“路由、交接、授权、上下文/缓存、失败恢复、可观测性”这些具体面上，谁更优，为什么？
5. 对 Freely 而言，哪些必须学、哪些必须改、哪些不能抄？

非目标：不评价模型能力，不复现文章实验，不用“自治程度高”这种无法判定的词下结论。

## 1. 结论先行

**没有全局更优的系统，只有对问题匹配度更高的系统。**

- **Super-agent 更优的地方**：事件级准入、注意力纪律、消息级交接（report/attention/handback/ownership）、prompt 前缀缓存纪律、单仓库内的响应速度。它把“不要打扰人”和“每条事件凭什么被处理”做成了运行时事实。
- **Freely 更优的地方**：规格驱动（SDD）、测试驱动（TDD）、独立 Reviewer、PR/merge 治理、多项目 fleet、harness 可替换。它把“这件事该怎么做、怎么验、凭什么合并”做成了文档与门禁事实。
- **Freely 的弱点是“运行时协作对象”不足**：没有 Trigger/Ticket/Mandate/Report/Attention/Disposition 这一层，消息归属、交接载荷、准入强度都偏粗。
- **Super-agent 的弱点是“交付治理”不足**：没有 B1/B2 规格层、没有 TDD 门禁、没有独立 Reviewer、只服务一个仓库，原型还缺 watchdog/存算分离。
- **对 Freely 的正确策略**：保留“文档是真相、TDD 是验收、Reviewer 是独立角色、门禁是合并前提”这四个差异优势；只借 Super-agent 的五个运行时 primitive，不整体迁移它的领域模型。

一句话：**Super-agent 是“团队助手的注意力预算系统”，Freely 是“项目所有者的交付治理系统”。** 前者优化“少打扰”，后者优化“可交付、可审计地闭环”。两者重叠在 agent 协作层，不在产品目标层。

## 2. 上层理念的共同点

| 共同问题 | Super-agent 的回答 | Freely 的回答 |
| --- | --- | --- |
| 人的注意力稀缺 | 默认沉默；只有可验收结果、必须决策、确实做不了才说话；IM 单条 ≤100 词 | 人定意图与验收；Manager 自主巡检，人通过 issue/chat/PR review 介入 |
| agent 要自己跑 | 常驻 Router + Worker；事件驱动；Watchdog（文章） | 常驻 Manager + Worker/Reviewer；three-loop + watchdog/continuation |
| 人从熟悉入口插话 | IM、GitHub 评论；回复回原会话 | GitHub/Gitee issue、`freely chat`/discuss、PR review |
| 上下文要连续 | 跨信道/跨任务保持一个 agent 的连续感；订阅 Thread | session resume/fork + 文档长期记忆 + worktree |
| 授权要有边界 | Policy + 准入表 + Mandate；谁能发起、做到哪 | 宪法/法律 + 角色 + 阶段 + 门禁 + 分支保护 |
| 并发不能互相踩 | 每 Ticket 一个 Session；多 Worker；订阅共享 Thread | 每 issue 一个 worktree + test 工位；Manager 派工 |
| 失败要能恢复 | effect 队列、恢复提示、未读 Input 重投 | supervisor/watchdog/continuation、session resume、门禁对账 |
| 结果要可检查 | Ticket stage、Decision/reason、Panel、health | 文档证据、测试证据、review verdict、PR/merge gate |

这些共同点说明：两者不是“谁更先进”，而是**同一组约束下的两种取舍**。

- Super-agent 把约束放在**运行时**：事件进来先过 gate，授权做成 Mandate，状态做成 Ticket stage，交接做成 Report/Attention。
- Freely 把约束放在**文档与流程**：规格写成 B1/B2，验收写成 pre-tests，合并交给 gate，角色由 agent 定义和 skill 约束。

## 3. 两种哲学

### 3.1 Super-agent：事件驱动、运行时授权、默认安静

它的第一性问题是：**一条环境事件，凭什么进入 agent、凭什么被处理、处理到哪、什么时候该打扰人。**

核心链条：

```
Source → Trigger → Thread → Eval(gate + assessment) → Decision
                                                   ├─ accept → Ticket + Mandate
                                                   ├─ ignore / stop / unavailable
                                                   └─ Subscription fan-out（只给上下文）
Ticket → Assignment → Executor Session → Report/Attention → Router
```

关键选择：

- gate 是代码，assessment 是模型；先快筛再慢判。
- 默认 `observe`：推断候选只记录“would accept”，不真的开工。
- Mandate 是不可变凭证；Policy 版本化；复活前重校验。
- Thread 订阅直通 Worker，绕过 Router/gate，但不授予新权限。
- Router 只分派，不读代码、不下实现指令；Worker 自己调查/实现/验证。
- 对外只由 Router 说话；Worker 的报告/问题先回 Router。

这套设计非常适合：**一个团队、一个仓库、持续有外部事件、需要控制打扰**。

### 3.2 Freely：文档驱动、生命周期治理、默认自主

它的第一性问题是：**一个项目从问题到合并，怎么在没有人盯着的情况下，仍然按规格、按测试、按治理闭环。**

核心链条：

```
issue / chat / 治理漂移
  → raw issue（平台副本，本地唯一真相）
  → B1_IBM：brainstorm → candidate → milestone
  → B2_IBM：I-* issue → PRD → pre-tests → tasks → code-review
  → dev-loop：RED → 实现 → test-GREEN
  → Reviewer：独立 verdict
  → pr-create → pr-review → pr-merge → wt-close
```

关键选择：

- **文档是状态**：platform 只是对外界面；scan 把平台下载成本地 `docs/B1-docs/`；AI 只读本地；sync 是本地→平台的唯一出口。
- **文档是驱动**：Manager 从 scan 得到 stage/next_action；Worker 从 issue/PRD/pre-tests 得到任务与验收；Reviewer 从产物得到审查对象。
- **TDD 是验收**：pre-tests 先写，RED 证明确实没实现/确实有 bug，GREEN 在 test-pre-merge 工位跑，门禁检查证据。
- **门禁是合并前提**：IBM 文档、测试、PR review、merge、closeout 各自有 gate；绕过 hook 被禁止。
- **角色分离**：Manager 调度、Worker 执行、Reviewer 独立审查；Reviewer 不站在任何一方。
- **worktree 隔离**：每个 issue 一个 dev 工位 + 一个可丢弃 test 工位。

这套设计非常适合：**长期运行、多项目、需要规格与审计、交付物要能被人类复核**。

### 3.3 两者不是同一根轴

| 轴 | Super-agent | Freely |
| --- | --- | --- |
| 优化目标 | 人的打断次数 / 响应时延 | 从问题到合并的自治闭环 / 可审计性 |
| 第一输入 | 环境事件 | 项目意图 + issue/chat + 治理信号 |
| 第一真相 | 运行时 DB（Trigger/Ticket/Decision） | 文档（intent/constitution/B1/B2/PRD/pre-tests） |
| 授权载体 | Mandate + Policy 版本 | 宪法/法律 + 角色 + 阶段 + 门禁 |
| 交付单元 | Ticket | issue + worktree + PR |
| 质量闸门 | 外部 review/CI + 人 | TDD + 独立 Reviewer + PR/merge gate |
| 适用边界 | 一个仓库、一个团队 | 多项目、长期治理 |

所以“Freely 应该更像 Super-agent”是错的；“Freely 应该吸收 Super-agent 的运行时协作 primitive”才是对的。

## 4. Freely 的真实架构：五个平面

这是 README 图应该表达的东西，也是之前那张图缺失的部分。

| 平面 | 组成 | 回答什么问题 |
| --- | --- | --- |
| 界面面 | GitHub/Gitee issue/comment、`freely chat`/discuss、CLI/TUI/GUI | 人从哪里进来、从哪里看结果 |
| 规格面（SDD） | PROJECT_INTENT、CONSTITUTION、LAWS、raw issue、B1 brainstorm/candidate、B2 PRD/pre-tests/tasks、code-review | 做什么、为什么、怎么验、边界在哪 |
| 控制面 | scan、Manager、three-loop、A2A、gates、watchdog、freely-db | 现在轮到谁、下一步是什么、能不能过 |
| 执行面 | Worker、Reviewer、worktree（dev/test）、TDD RED/GREEN、commands/scripts/skills/MCP | 实际怎么干、怎么验证 |
| 基座面 | ACP harness（Claude/Codex/OpenCode/Cline）、GitHub/Gitee | 用什么执行、外部世界在哪 |

实际控制流：

1. 人在 issue/comment/chat 里提出请求；platform 是界面，不是 AI 的真相源。
2. `scan` 把平台内容下载到本地 `docs/B1-docs/`，并推导 `stage` / `next_action`。
3. Manager 读 scan + 工位/任务状态 + 文档，决定建 raw issue、建工位、派 Worker、或收口。
4. B1 把 raw issue 收敛为 candidate；B2 把 candidate 物化为 I-* + PRD + pre-tests + tasks。
5. Worker 在 dev worktree 按 pre-tests 先 RED 再实现；test-pre-merge 工位跑 GREEN。
6. Reviewer 独立审查；verdict 回 Manager/Worker。
7. `pr-create-guarded` / `pr-review-guarded` / `pr-merge-guarded` / `wt-close` 完成合并与收口。
8. 文档、milestone、`phase_state`、A2A task、测试证据一起更新。

**关键点：Freely 不是“runtime 驱动一切”，而是“文档定义状态与规格，runtime 执行调度，gate 验证证据”。** README 图如果只画 Manager/Worker/gate，会漏掉最重要的规格面与 TDD 面。

### 4.1 各层的职责边界

- **文档**：长期记忆、规格、验收、审计证据；不直接执行。
- **runtime/script**：确定性调度、scan、状态搬运、gate 执行；不做价值判断。
- **skill**：把流程、角色、门禁知识编码成 agent 可加载的指令；不是权限。
- **command**：封装多步治理动作（feedback/wt-create/pr-*/wt-close）；不是普通 CLI 糖。
- **MCP**：agent 与外部工具/资源的连接；不是 agent 间编排。当前 `run-acp-prompt.py` 对 ACP 会话传 `mcpServers: []`，Freely 不编排 MCP；是否可用取决于底层 AI CLI 自己的配置。
- **agent harness（ACP）**：真正跑模型会话的执行提供层；可替换，不是 Freely 的宿主。
- **A2A**：Manager/Worker/Reviewer 的任务协调；不是文档真相源。
- **gate**：对文档/测试/PR/merge 的硬检查；不是提示词建议。

这八者混在一起，就会得到一张“看起来什么都画了、实际什么都没说清”的架构图。

## 5. Super-agent 的真实架构：五个模块与原型边界

| 模块 | 文章主张 | 原型实现 |
| --- | --- | --- |
| 双层 | Router 只分派，Worker 隔离执行 | 有；Router/Worker Session + preset |
| 事件驱动 | Source/Trigger/Thread/Eval + Fast/Slow Path | 有；gate + assessment + 准入表 |
| 订阅直通 | Thread 事件绕过 Router 直达 Worker | 有；Subscription + handback |
| 异步多信道 | start/stop 异步 ReAct，按信道定制话术 | 只有后台 job，异步 ReAct 未默认开启 |
| 存算分离 | 计算/状态/环境解耦，云端持久 | 未实现；单机 stateDir |
| 外部 Watchdog | 独立 agent 判断进展 | 未实现 |
| 通用多仓 | 无 | 单 GitHub 仓库 |
| 独立 Reviewer | 无 | 无；Worker 自审 + 外部 bot |
| 规格/TDD | 无 | 无 |

结论：**文章是架构论文，原型是可运行子集。** 比较时必须区分“文章说要做”和“原型已经做”。

## 6. 逐维对比与判定

| 维度 | Super-agent | Freely | 判定 |
| --- | --- | --- | --- |
| 注意力 | 默认沉默；结构化 attention；IM ≤100 词 | Manager 主动汇报；scan needs_human；chat/issue 入口多 | **Super-agent 更优**：打扰控制更硬 |
| 自主发现 | 规则 + 推断候选；默认 observe | scan + 治理漂移 + runtime 异常；默认自主 | **Freely 更广，Super-agent 更稳** |
| 人插话 | IM/GitHub；回原会话 | issue/comment/chat；discuss | 平手；Freely 入口更多，Super-agent 归属更清 |
| 事件准入 | 代码 gate + 模型 assessment | 无 per-event gate；Manager 判断 | **Super-agent 更优** |
| 授权 | Mandate + Policy 版本 + 重校验 | 宪法/法律 + 角色 + 阶段 + 门禁 | **分层不同**：单事件 Super-agent 强；合并治理 Freely 强 |
| SDD | 无规格层 | B1/B2/PRD/pre-tests/tasks/code-review | **Freely 明显更优** |
| TDD | 无 | RED/GREEN/test-pre-merge/pretests gate | **Freely 明显更优** |
| 交接 | 六态 report + attention + handback + ownership | A2A state + summary/evidence + Reviewer verdict | **Super-agent 消息级更优；Freely 阶段级更完整** |
| 路由 | 代码 gate + 1–20 批量决策 + 逐条拒绝 | scan 推导 stage + Manager 派工 | **Super-agent 运行时更硬；Freely 生命周期更准** |
| 上下文 | Inline/Spill + 链式召回 + 前缀稳定 | 文档长期记忆 + session fork/resume | **分裂**：DSH 单会话更精；Freely 跨会话/跨项目更久 |
| 缓存 | 段序固定、Policy 置尾；无 cache 指标 | fork/resume；有 `[CACHE]` 但多为估算 | **分裂**：DSH 纪律好，Freely 可观测但不可控 |
| 并发 | Worker slot + 人优先槽位 + Thread 共享 | worktree 隔离 + worker pool + fleet | **仓库内 DSH 细；跨项目 Freely 广** |
| 失败恢复 | effect 队列 + 恢复提示 + 未读 Input | supervisor/watchdog/continuation + gate 对账 | **分裂**：外部副作用 DSH 强；进程/工位 Freely 强 |
| 可观测 | 单写 DB + health board + panel | 文档 + CLI status + DB + 审计 | **分裂**：实时 DSH 强；审计 Freely 强 |
| Harness | 绑定 Cordis/DSH，无 ACP | ACP 多 CLI 可替换 | **Freely 更优**（但契约仍是隐式） |
| 规模 | 单仓单团队 | 多项目 fleet | **Freely 更广，DSH 更深** |

### 6.1 按场景判定：谁更优秀取决于问题

| 场景 | 更优 | 为什么 |
| --- | --- | --- |
| 一个仓库、一个团队、事件很多、怕打扰 | Super-agent | 代码 gate + observe + 订阅直通 + 注意力纪律 |
| 多项目、长周期、要规格与审计 | Freely | SDD + TDD + Reviewer + PR/merge 门禁 + fleet |
| 一条明确的 bug，今天就要修 | Super-agent | 无 B1/B2/PRD 开销，直接 Ticket→Worker |
| 一条模糊需求，需要先收敛边界 | Freely | B1 brainstorm/candidate 强制先想清楚 |
| PR 里后续讨论很多，怕漏接 | Super-agent | Thread 订阅 + followupOwners + handback |
| 合并前要证明测试真的跑过 | Freely | pre-tests + test-pre-merge + pretests gate |
| 团队要换 AI CLI / 不被一家 harness 锁定 | Freely | ACP 多 CLI；DSH 绑定 Cordis |
| 需要单仓库内极低延迟的多事件调度 | Super-agent | 单 Router 批处理 + 订阅直通 |
| 需要跨项目调度与人机审计 | Freely | fleet + 文档证据链 |

结论：**如果问题是“团队助手的注意力与事件响应”，Super-agent 的方案更合适；如果问题是“项目所有者的交付治理”，Freely 的方案更合适。** 两者可以组合，但必须定“一个 loop 一个 owner”。

## 7. 深水区

### 7.1 路由与准入：DSH 赢在“先判后做”，Freely 赢在“知道现在该做什么”

DSH：

- 代码 gate 先判发送者/来源/准入表/机器人；模型只处理候选。
- `orchestrator_route` 1–20 条批量决策，逐条校验、逐条事务、单条失败不影响其他。
- accept 以 trigger ID 幂等；note ≤30 词、ack ≤100 词由 schema 限制。
- 显式请求可直接 accept；推断候选必须走完整 assessment。

Freely：

- scan 从文档/phase_state/milestone 推导 stage 与 next_action；这是生命周期级路由，比 DSH 的 topic 级更懂“这活到哪一步”。
- Manager 读 scan + A2A + fleet；没有 per-event gate，也没有批量决策协议；效率取决于 Manager 的上下文与纪律。
- 幂等靠 `a2a_task list --raw-key` 查询，不是事件级账本。

判定：**单条事件该不该做，DSH 更硬；一个项目下一步该做什么，Freely 更准。** Freely 应补“事件准入 + 批量决策 + 幂等键”，但不放弃 scan 的 stage 路由。

### 7.2 交接：DSH 是消息级，Freely 是任务级

DSH：

- Report 六态；Attention 单问题 + 目标会话；`followupOwners` 决定谁拥有后续消息；Worker 可 handback 一次；relay 有稳定 key 去重。
- Worker 不直接对外说话；Router 统一回复。
- 订阅 Thread 的消息直达 Worker，绕过 Router/gate，但不授权。

Freely：

- A2A 有状态机；Reviewer verdict 通过 SSE 广播；Manager 可 session/prompt 纠偏；3 次失败升级。
- 但 summary/evidence 是自由文本；没有“这条消息归谁”的运行时事实；没有消息级 handback。
- Reviewer 是独立角色，这是 DSH 没有的。

判定：**消息级交接 DSH 更细；阶段级质量交接 Freely 更完整。** Freely 应补类型化 report/attention/ownership，但不能把 Reviewer 换成“Worker 自审”。

### 7.3 SDD：Freely 的最强差异，也是最大成本

Freely 的 SDD 不是“写文档”，而是：

- 文档是状态：平台只是界面，本地 `docs/B1-docs/` 是真相；scan 下载，sync 上传。
- 文档是驱动：Manager 从 scan 得到下一步；Worker 从 issue/PRD/pre-tests 得到任务与验收。
- 文档是证据：B1/B2、PRD、pre-tests、code-review 都是合并/收口的依据。
- 文档是边界：CONSTITUTION/LAWS 是不可协商约束。

DSH 没有这一层：Ticket 有授权与执行，但没有“为什么做、怎么验、替代方案、边界”的规格产物。

代价：文档多、更新慢、容易漂移；对 tiny task 过重。收益：长期可审计、可交接、可让新 agent 快速接手。

但“文档驱动”也要分层看：

- **状态层**：scan 确实从 docs/phase_state/milestone 推导 next_action；这一层是文档驱动。
- **执行层**：Manager/Worker 的 prompt 主要是 agent 定义 + 任务/scan + skill；PRD/pre-tests 不会自动注入，靠 skill 要求 agent 去读。也就是说，文档是“规格与验收的真相”，但不是每一轮 prompt 的自动上下文。
- **门禁层**：IBM gate 在 PR/merge 时检查文档存在与格式，不检查实现是否真的按 PRD 做；文档可以在实现后补。它是“合并前必须齐”，不是“写代码前必须读”。

判定：**Freely 的 SDD 明显优于 DSH 的空缺；但它是“状态 + 门禁”驱动，不是“每步 prompt 自动文档驱动”。** 需要治理文档漂移、backfill 与开销。不能为了“轻”退回 Ticket-only。

### 7.4 TDD：Freely 的第二个强差异

Freely 的 pre-tests 是验收合同：

- B2 写 pre-tests；RED 证明未实现/可复现；dev 实现；GREEN 在 test-pre-merge 工位跑；pretests gate 检查证据；review 再查。
- test-pre-merge 是可丢弃沙箱；dev↔test 必须一致；PR 前必须 GREEN。

DSH 没有 TDD：Worker 自己决定测试，CI 是外部；没有“先 RED 再实现”的强制环。

但 Freely 的实现也要看清：`pretests-gate` 强制的是**终态** `red-green-status=green` 或合法的 `not_applicable`；它并不检查 `actual_RED_output` 是否真实，也不检查提交顺序是否“先 RED 后实现”。RED 阶段由 `freely-test-RED-execution` skill 驱动，是流程约束，不是独立的 runtime gate。所以 Freely 的 TDD 更准确的说法是“**流程 + 终态证据门禁**”，不是“每个提交都机器证明先 RED”。

判定：**Freely 明显优于 DSH 的空白**，尤其对“AI 写代码容易自证”的问题；但不要把它吹成完全硬保证。代价是流程重、慢；对 docs-only/极小改动允许 not_applicable，但不能变成默认免检。

### 7.5 上下文与缓存：DSH 纪律好，Freely 记忆长

DSH：

- 固定段序，Policy 置尾；覆盖记录 base；每次请求绑定 revision；prefix 稳定。
- 评估窗口有界（首 5 + 前后 5）；文本截断留续读入口；对象 ID 链式召回。
- Router/Worker 各自 Session；Worker 冷启动；没有 cache 指标。

Freely：

- session resume/fork；worker/reviewer fork manager 继承治理上下文；文档是长期记忆；worktree 是环境隔离。
- 但 prompt 是“角色定义 + 运行时状态”拼接；scan/fleet/checkpoint 追加在尾部；没有 stable_prefix/volatile_tail 契约。
- `[CACHE]` 日志有，但 input 常是 `prompt_bytes//4` 估算，hit/miss 常为 0；不能当真实命中率。

判定：**单会话上下文纪律 DSH 更优；跨会话/跨项目长期记忆 Freely 更优。** Freely 应把 prompt 拆成稳定前缀/可变尾部，并区分 usage/estimated。

### 7.6 授权：不是谁“更安全”，而是防守点不同

DSH 防“这条事件不该被处理 / 这个范围不该做”：gate、Mandate、Policy 版本、复活重校验。

Freely 防“这个改动不该合并 / 这个阶段不该跳过”：角色、phase、IBM 文档、pre-tests、reviewer、PR/merge gate、分支保护。

判定：**DSH 的运行时授权更强；Freely 的组织治理更强。** Freely 不需要复制 Mandate，但应记录“这次工作凭什么被批准、范围是什么、依据哪版规则”，让审计不必从文档里拼。

### 7.7 Harness/插件：Freely 的架构优势，DSH 的深度优势

Freely：

- ACP 适配 Claude/Codex/OpenCode/Cline；session/new/resume/fork；usage/cache 部分可用。
- runtime 不绑定某家 CLI；agent harness 是执行层。
- 但契约是隐式的：能力差异靠分支兜底；没有 capability probe；DSH 没有 adapter。

DSH：

- Cordis bundle，深度使用 DSH Session/Agent/Tool/Preset/Client API；插件面强。
- 但绑定 DSH，`engines.dsh` 钉版本；没有 ACP 服务端；换宿主是重写。

判定：**Freely 的“可替换基座”方向更对；DSH 的“单宿主深度”更强。** 优先级应是 Freely 内 HarnessPort 正式化，再谈 DSH adapter；DSH 插件只做工具外溢，不做第二套 Router/Ticket。

### 7.8 实证检查（2026-11-01，本工位）

不是所有结论都能从文档推出来，这一轮做了四个实测：

1. **`freely task-source-scan --json` 的 station 与 next_action 不一致，且 worktree 维度重复。**
   本工位扫描返回 4 个 item，全部标成 `收口`：对应 3 个 raw key 的 dev/test 工位尚未清理，同一 raw 因两个工位各出现一次。这个“收口”本身是合理的（worktree not cleaned），但 next_action 仍是 `wt-create --raw-key ...` / 进入 B1，和 station 不匹配。同时 `platform_health=degraded`，原因是 `No module named 'platform_adapter'`。
   结论不是“scan 完全误判”，而是：**scan 能识别 worktree 未清理，但 next_action 渲染没有跟 station 对齐，也没有按 raw key 去重。** 这属于“文档状态 → 动作”的转换层缺陷。
   注意：fleet 里已有专门修 `scan-platform-adapter-import` 的工位（`fix-raw-20260807T114900Z-scan-platform-adapter-import`），`platform_adapter` 缺失是已知在修问题，不能归因于架构设计；需修复后复测。

   另外，CLI usage 里列了 `freely task-scan`，实际 dispatch 报 `unknown command: task-scan`；这是文档/命令面与 runtime 的不一致，属于可观测的漂移样本。

2. **TDD 证据不均匀。**
   当前 `docs/B2-docs/**/pre-tests.md` 共 431 份，其中 327 份出现 `not_applicable`，247 份没有 `test_command`。这不能直接判为“TDD 失败”（很多是历史 schema 或 docs-only 变更），但说明“TDD 是强制验收”在历史资产里并不均匀；新门禁只覆盖新产物，不能把历史绿当成整体绿。

3. **缓存是估算，不是实测。**
   主项目最近 50 个 cycle 的 21 条 `[CACHE]` 全部满足 `input == prompt_bytes // 4`，`hit/miss=0`；`harness-status` 现在会标 `input_source=estimated`。所以“Freely 的 cache 可观测”只对“是否上报”成立，对“命中率”不成立。

4. **Reviewer 的 fork 是降级，不是 native。**
   `freely harness-status --require fork` 在主项目失败：reviewer 用的 Cline 是 `degraded=fork`。这不是“Reviewer 不能工作”，而是“Reviewer 首轮必须冷启动或走 session/new”，与文档里“fork 继承治理上下文”的默认叙事有差距。

这些实测是下一轮设计（事件准入、ownership、TDD 适用范围、HarnessPort）的事实基础，不是实现任务。

### 7.9 治理格式分裂：同一个 I-* 被两个门禁用两种方式解析

这一轮修 I-* 时发现一个结构性问题：

- `pretests-gate` 的 `phase_state()` 只认正文 bullet：`^- phase_state:`。I-* 若只有 YAML frontmatter，完成门禁会读不到 phase，静默放行。
- `pr-merge-guarded` 的 `_update_issue_phase` 和 issue sync 只读 YAML frontmatter：`split('---',2)` 后 `yaml.safe_load`。I-* 若只有 bullet，`kind`/`phase_state` 为空，merge 时不会同步/关闭 issue。
- 结果是：**同一个 I-* 必须同时写 YAML frontmatter 和正文 bullet**，两个门禁才都能读到。B2 skill 里提到“frontmatter 与正文 bullet 都要写”，但这不是一个显式 schema，也没有一个校验器同时检查两者一致。

`phase_state` 的写入者也不止一个：`wt-create` 会把 raw 改回 `proposed`，`pr-review-guarded` 把 `done_b2_ibm` 改成 `completed`，`pr-merge-guarded` 在 merge 前改 `absorbed`/`in_verification`，`wt-close` 只检查、不改。**没有单一写者，也没有“谁有权改哪个 phase”的显式表。**

这不是一个字段 bug，而是“文档作为状态机”缺少 schema/单写者契约的证据。Super-agent 的 Ticket 状态由 Engine 唯一写；Freely 的 phase 由多个脚本各写一段。前者状态更可靠但绑定运行时；后者可审计但容易漂移。Freely 要补的不是更多文档，而是**状态 schema + 单写者/派生规则**。

### 7.10 状态权威不是“一份真相”，而是“分域真相”

“docs 是唯一真相”这个说法不够准确。读 `task-lifecycle-scan.py` 的设计原则和实现后，Freely 实际是**分域真相 + scan 对账**：

| 问题 | 权威源 | 谁写 | 说明 |
| --- | --- | --- | --- |
| 做什么、为什么、怎么验、边界 | docs（Intent/Constitution/LAWS、B1/B2、PRD/pre-tests） | B1/B2、人、Worker | 规格与生命周期的真相 |
| 现在有没有 agent 在做 | A2A `sessions`/`a2a_tasks` | runtime/A2A server | scan 明确写“A2A is the arbiter of in progress”；活跃会话不被扫描 |
| 生命周期到哪一步 | issue `phase_state` + milestone | wt-create、pr-review、pr-merge | 多写者，容易漂移 |
| 代码/工位是否存在 | git worktree/branch | git、wt-create/wt-close | 环境真相 |
| 测试是否在 HEAD 跑过 | `.freely/run/test-gate.env` + evidence | daemon stop、test-lane | 证据真相 |
| 对外平台状态 | GitHub/Gitee | issue-sync/platform-adapter | 对外副本；AI 只读本地复制 |
| 下一步是什么 | scan 的 stage/next_action | scan 派生 | 派生视图，不是权威源 |

这与 Super-agent 的“单写者 DB”是根本差异：

- DSH：Engine 是 Trigger/Ticket/Decision 的唯一写者，状态在一个地方，查询精确；代价是绑定运行时。
- Freely：不同问题有不同权威源，文档可审计、A2A 实时、git 可验证；代价是**必须持续对账**，否则 phase/scan/milestone 会互相矛盾。

所以 Freely 的问题不是“文档不够多”，而是**缺少一张权威矩阵 + 派生规则**：哪个字段由谁写、哪些是派生、冲突时谁赢。这比再加一个 gate 更根本。

### 7.11 人插话入口：四条路，只有两条是真正闭环的

| 入口 | 实际路径 | 谁处理 | 是否闭环 | 差距 |
| --- | --- | --- | --- | --- |
| 新建 issue/comment | platform-adapter → scan → 本地 `docs/B1-docs/` | Manager → B1 | 新建 issue 闭环；comment 取决于 pull/scan 是否刷新 | 没有 per-comment 事件与归属 |
| IM / `freely chat` | `freely chat` → `freely.db chats` → Manager prompt 的 chat snapshot | Manager | 闭环 | 不直达 Worker；靠 Manager 二次路由 |
| PR review comment / CI 反馈 | 不在 platform-adapter 的 review-comment 读取面；GitHub review 是外部 merge gate | 人 / GitHub | 不闭环 | 后续讨论可能没人拥有；这是最大缺口 |
| CLI/会话内插话 | `a2a_task.py prompt` / 人直接进 executor session | Manager 或 Worker | 部分 | 不是普通人的入口，偏运维 |

对照 Super-agent：

- IM/GitHub 消息都是 Trigger；订阅 Thread 的消息直达 Ticket 的 Worker；人消息可复活已结束 Ticket；handback 决定归属。
- Freely 的 chat 入口是完整的，但 issue comment 与 PR review 没有“消息级 ownership”；后者甚至没有进入 runtime 的自动路径。

结论：**Freely 的“人插话”在入口数量上不输，但在“后续消息归属”上明显弱于 Super-agent。** 这不是再加一个 CLI 能解决的，需要 ownership 账本或订阅层。

### 7.12 多项目 fleet 的实测边界

- `~/.freely/projects.tsv` 真实存在，包含大量项目登记；Freely 确实有跨项目 registry。
- 但 `freely fleet-status --project <one>` 只列“这个 project 的 worktree 列表”（develop、feature、fix、test-pre-merge），不是跨项目总览。
- 没有看到统一的“所有项目的 health/任务/注意力”视图；跨项目操作更多是运维脚本层（`restart --all-projects` 等）。

所以“多项目 fleet”要分两层说：

- **项目登记/独立 runtime**：真实存在，是 Freely 相对 DSH 的差异。
- **跨项目统一调度与注意力视图**：目前不是产品面，不能把它当成已完成能力写进 README。

README 已改为“全局 projects.tsv 登记；fleet-status 是本项目工位视图，不是跨项目调度台”。

## 8. Freely 明确不如 Super-agent 的地方

1. **事件级准入**：没有代码 gate；Manager 可能被长上下文说服。
2. **消息级交接**：没有 report 六态/attention/ownership/handback。
3. **注意力纪律**：Manager 主动汇报多；缺少“默认沉默”的硬约束。
4. **prompt 前缀纪律**：没有 stable prefix 契约；cache 多为估算。
5. **外部副作用幂等**：没有 effect 队列/统一 receipt。
6. **文档漂移**：docs/phase_state/milestone/scan 多源，需持续对账。
7. **文档开销**：SDD/TDD 对 tiny task 过重。

## 9. Super-agent 明确不如 Freely 的地方

1. **没有 SDD**：没有 B1/B2/PRD/pre-tests/tasks 的规格层。
2. **没有 TDD**：没有 RED/GREEN/test-pre-merge 的强制验收。
3. **没有独立 Reviewer**：Worker 自审 + 外部 bot。
4. **没有合并治理**：没有 PR/merge/closeout 门禁链。
5. **单仓库/单机**：多项目、多工位不适用。
6. **原型缺口**：watchdog、存算分离、异步 ReAct 未落地。
7. **插件锁定**：Cordis/DSH 深度绑定，换宿主成本高。

## 10. 对 Freely 的取舍

| 判断 | 机制 | 理由 |
| --- | --- | --- |
| 必须学 | 事件准入 + 决策强度 | 补 Freely 最弱的运行时防守；但不复制 Mandate 全量 |
| 必须学 | 消息级 report/attention/ownership/handback | 补 follow-up 丢失/重复开单 |
| 必须学 | 路由批处理 + 逐条拒绝 + 幂等键 | Manager 上下文与吞吐的现实解 |
| 必须学 | prompt 稳定前缀/可变尾部 + usage/estimated | 让 cache 可度量、可回归 |
| 可适配 | Thread 订阅直通 | 先做“同一工单线程 ownership”，不做事件总线 |
| 可适配 | Policy 版本 | 记录“依据哪版规则批准”，不做运行时 Mandate |
| 可适配 | DSH adapter | 作为 HarnessPort 的一个实现；不让 DSH 接管 three-loop |
| 可适配 | Freely 工具作为 DSH 插件 | 只外溢 gates/worktree/issue，不起第二套调度 |
| 不照搬 | 默认 observe / 默认不做 | 与 Freely “项目所有者”目标冲突 |
| 不照搬 | 单仓/单机 | 与多项目 fleet 冲突 |
| 不照搬 | 移除 Reviewer | 削弱质量分离 |
| 不照搬 | 事件溯源重写 | Freely 的治理证据在文档与平台 |
| 不照搬 | 双 Router/Ticket | 插件化最大陷阱 |

## 11. 还没研究透、下一轮必须回答的问题

1. **文档是唯一真相，还是文档+DB 双真相？** 现在 phase_state/milestone/scan/A2A 多源；哪个该是派生、哪个该是权威？
2. **事件准入放在哪一层？** scan 前、Manager 前、还是 raw issue 创建时？会不会与 SDD 的 B1 价值判断重复？
3. **TDD 的适用范围**：docs-only、极小改动、紧急 hotfix 是否允许 not_applicable？如何防止“默认免检”？
4. **注意力成本怎么度量？** Manager 主动汇报次数、人工介入时长、误报/漏报，哪个是主指标？
5. **HarnessPort 的能力契约**：哪些能力是必需、哪些可降级？DSH adapter 走 in-process 还是子进程？
6. **多项目 fleet 是不是真差异**：用户是否真的需要跨项目调度，还是单项目深度更重要？
7. **文档漂移的根因**：是 scan 推导不完整，还是 phase_state 写入不受单一写者控制？
8. **Freely 的“自主”边界**：哪些决定必须人批？哪些可以 agent 自批？和 DSH 的 observe/auto 如何映射？

## 12. 证据索引

| 事实 | 来源 |
| --- | --- |
| 文章五模块、实验数字 | 智东西 `https://www.zhidx.com/p/606311.html`；博客园 `https://www.cnblogs.com/itech/p/23508901` |
| 原型范围、单仓、无 ACP | `README.md`、`docs/006-deployment.md`、`package.json`、`cordis.patch.yml` |
| 领域模型、拒绝概念 | `docs/001-domain.md` |
| 准入表、observe/auto、Policy 版本 | `docs/002-authorization.md` |
| Ticket stage、worker slot、恢复 | `docs/003-execution.md` |
| Prompt 分层/Policy 置尾 | `docs/004-prompts.md`、`src/app/prompts.ts` |
| 路由批处理/幂等 | `src/app/tools/main.ts`、`prompts/dispatch.md` |
| Report/attention/relay key | `src/app/notices.ts` |
| 订阅/handback/ownership | `prompts/subscriptions.md`、`docs/002-authorization.md` |
| Freely SDD/IBM | `docs/system/workspace/ibm-framework.md` |
| Freely three-loop | `docs/system/workspace/three-loop-capability-lifecycle.md` |
| Freely scan/平台隔离 | `docs/system/workspace/scan-lifecycle-design.md`、`ibm-framework.md` §平台隔离 |
| Freely TDD | `docs/system/workspace/skills/freely-test-RED-execution/SKILL.md`、`freely-test-execution/SKILL.md`、`pretests-gate` |
| Freely harness/ACP | `docs/system/workspace/tools.md`、`acp-session-architecture.md`、`run-acp-prompt.py` |
| Freely 角色 | `docs/system/workspace/agents/*.md` |
| Freely A2A | `docs/system/workspace/a2a/*` |
