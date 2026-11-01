---
analysis_id: OVERLAP-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 重叠意图对照：Super-agent 的思路、架构、实现 vs Freely

## 0. 比较边界

Freely 是 **code harness**，实现范围比 Super-agent 大：

- Freely 有 SDD/TDD、B1/B2、独立 Reviewer、PR/merge gate、worktree/test lane、多项目 registry；
- Super-agent 有 Router/Worker、Trigger/Thread/Subscription、Report/Attention、Mandate、Watchdog、云端/多设备。

本文件**只比较意图重叠的部分**：

1. 主动发现：环境事件 → 是否值得做。
2. 分派：谁决定、怎么派。
3. 执行隔离：Worker 怎么跑、怎么汇报。
4. 连续：跨讨论/跨轮次上下文归谁。
5. 交接：消息、状态、owner、handback。
6. 授权：谁能发起、做到哪。
7. 持久：异常/重启/跑偏怎么恢复。
8. 上下文：窗口、文档、缓存。

Freely 多出来的能力不拿来证明“谁更强”；Super-agent 的个人助手/云端/IM 部分也不算 Freely 的缺口。

## 1. 三篇解读的差异（只取与重叠意图相关的部分）

| 维度 | 智东西 | IT之家 | 驱动中国 |
| --- | --- | --- | --- |
| 系统层 | 最重：批处理、Fast/Slow、缓存、存算分离 | 中等 | 概览 |
| Router | 可轻量、可不全是 LLM；批处理扛突发 | Router/Worker 分工 | 同 |
| 事件 | Trigger/Eval、订阅直通、Inline/Spill、链式召回、投机执行 | 两级过滤、订阅 | 事件驱动、订阅 |
| 交接 | Worker 不直接对外；Report/Attention | 同 | 同 |
| 持久 | 存算分离、BYOM、外部 Watchdog | 同 | 同 |
| A2A | 明确列为开放问题 | 未展开 | 未展开 |

结论：**智东西最接近“系统设计意图”，IT之家/驱动中国更偏产品概括。** 比较实现时以原型代码 + 智东西细节为准，不用媒体标题当结论。

## 2. 共同意图（先对齐）

两边都在解决：

> 人的注意力是瓶颈；Agent 要持续在线、主动发现、并行推进、跨轮次保持上下文，并在异常后恢复。

但落点不同：

- Super-agent：**系统层接管 Session 调度与上下文**，让一个 Agent 跨渠道连续。
- Freely：**项目层接管交付**，让 AI 按 SDD/TDD 维护规格/测试并推进到 PR。

所以 Freely 的比较对象不是“Super-agent 全部”，而是它的 **事件/分派/交接/持久/上下文** 这一段。

## 3. 叫法不同，问题相同：概念对照

| Super-agent | Freely | 是否同一问题 | 差异 |
| --- | --- | --- | --- |
| Source / Trigger | scan 输入、issue/chat/PR/CI | 是 | DSH 事件级；Freely scan 批量，且未接评论/PR/CI |
| Eval / gate / assessment | Manager + B1 判断；scan 预筛 | 是 | DSH 代码 gate + 模型 assessment；Freely 无 per-event gate |
| Router | Manager | 是 | DSH 更窄（只分派/对外）；Freely Manager 还巡检/建工位/收口 |
| Worker / Assignment | Worker / A2A task / worktree | 是 | DSH Assignment 独立状态；Freely 压进 a2a_tasks |
| Thread | issue/PR/chat 线程 | 是 | DSH 有 Thread 对象；Freely 无线程对象 |
| Subscription / followupOwners | 无直接对应（C-B/C-F） | 是 | DSH 后续消息直达 Worker；Freely 靠 Manager/新单 |
| Report / Attention | A2A summary / input-required | 是 | DSH 六态 + 单问题；Freely 自由文本/覆盖 |
| Mandate / Policy | Constitution / Laws / gates | 是 | DSH 运行时授权；Freely 流程/文档治理 |
| Watchdog | supervisor / watchdog_sse / continuation | 是 | DSH 文章是独立语义 Watchdog；Freely 是进程/SSE 路由 |
| Inline & Spill / Chain of Recall | docs + prompt 排序 | 是 | DSH 管窗口；Freely 管长期文档 |
| Effect queue | issue-sync / retry | 是 | DSH 持久 effect；Freely 无通用 effect 队列 |
| Speculative execution | 无 | 否 | 不属于 Freely 主意图，不必照搬 |
| Async ReAct | 无完整对应 | 否 | Worker/Manager 是异步 session，但不是全双工 |
| Cloud / BYOM | 无 | 否 | Freely 本地 worktree，主意图未要求云端 |

## 4. 逐项评审

### 4.1 主动发现：DSH 更强，Freely 的 scan 是“半主动”

**Super-agent**：

- Source → Trigger → gate（代码）→ assessment（模型）→ Decision。
- Fast Path 过滤大部分噪音；Slow Path 只判候选。
- Trigger 是事件级，有 actor/来源/强度；天然支持 issue 评论、PR review、CI。
- 可以 observe 记录“would accept”，不打扰人。

**Freely**：

- scan 是批量/轮询，先读 docs/phase/platform，再给 Manager 一个 stage/next_action。
- 没有 per-event gate；Manager 读 scan 后判断。
- **scan 目前不处理 issue comment/PR review/CI**；只处理 issue body + chat DB。
- 所以“主动”是 Manager 主动，不是 scan 级事件主动；讨论场景会漏。

**判定**：Super-agent 的事件层更强；Freely 的生命周期判断更强。**吸收事件级入口/准入，不放弃 scan 的 stage 判断。**

### 4.2 分派：DSH Router 更轻，Freely Manager 更宽

**Super-agent**：

- Router 只承接人、维护全局上下文、分派；不读代码、不做实现。
- 批处理 1–20 条 Trigger，单条失败不影响其他；accept 按 trigger ID 幂等。
- 轻量模型即可。

**Freely**：

- Manager 还负责巡检、建 raw issue/工位、收口、升级；职责更宽。
- 有 A2A task，但没有批量决策/逐条拒绝/事件级幂等。
- Manager prompt 容易变重；需要 scan/fleet/checkpoint 纪律。

**判定**：DSH 的路由更“窄而快”；Freely 的 Manager 更“宽而重”。**吸收批量决策 + 幂等键 + 明确“不读代码/不下实现指令”，但不把 Manager 缩成纯 Router。**

### 4.3 执行隔离：两边都强，DSH 的 Assignment 状态更干净

**Super-agent**：

- Worker 每 Ticket 一个 Session/目录；Worker 不直接对外；Report 回 Router。
- Assignment pending/running/ended 与 Ticket 状态分离。
- 失败/阻塞/恢复有明确阶段。

**Freely**：

- Worker/Reviewer 独立 session/worktree；Reviewer 独立审查，这是 Freely 的额外优势。
- 但 `a2a_tasks` 一行同时承担 task 状态、执行者、message、summary；Reviewer verdict 覆盖 Worker summary。
- `acp_session_connect` new/fork 不发送 message；首次交接会丢。

**判定**：隔离都强；**交接状态模型 DSH 更干净**。Freely 应吸收 Assignment/Report 分离，保留 Reviewer。

### 4.4 连续：DSH 有 Thread/Subscription，Freely 只有文档

**Super-agent**：

- Thread 是时间序事件流；Subscription 多对多；后续消息直达 Worker，不经 Router。
- followupOwners 决定谁拥有后续消息；handback 明确交回。
- 未读 Input 重投；已结束 Ticket 可被人的消息复活（在 Mandate 内）。

**Freely**：

- issue/PR/chat 是入口，但没有 Thread 对象/订阅；后续讨论靠 Manager 或新开单。
- chat 进 Manager prompt；issue comment/PR review 不进 runtime。
- 文档提供长期记忆，但不是“消息归属”的运行时事实。

**判定**：**DSH 明显更强**。这是 Freely 最该补的连续/交接能力（C-F + C-B）。

### 4.5 交接：DSH 类型化，Freely 自由文本

**Super-agent**：

- Report 六态：progress/waiting/ready/blocked/failed/dropped。
- Attention：单问题、目标会话、human_action、question_for_trigger_id。
- relay key 去重；ownership/handback；未读重投。

**Freely**：

- A2A state + `summary/reason/next_action/evidence_paths` 自由文本；Reviewer verdict JSON 契约不统一。
- 没有 per-message id/append-only；task 行 update 覆盖。
- 没有“这条消息归谁”的 owner 字段。

**判定**：**DSH 更强**。Freely 的 delegation-protocol v0 已给出 envelope/ownership，但未实现。

### 4.6 授权：DSH 运行时准入，Freely 流程治理

**Super-agent**：

- Policy 版本 + 准入表 + Mandate（scope/strength）；gate 在模型前拒绝。
- 复活重校验；Policy 变化不吊销 Mandate，但会送达。
- 强在“一条事件能不能做、做到哪”。

**Freely**：

- Constitution/Laws + 角色 + phase + IBM/TDD/PR/merge gates。
- 强在“一个改动能不能合并、有没有规格/测试/审查”。
- 没有 per-event 准入；Manager 可能被长上下文说服。

**判定**：**分层不同**。单事件 DSH 强；交付治理 Freely 强。Freely 应补轻量 admission（来源/actor/强度/幂等），不抄 Mandate 全量。

### 4.7 持久：DSH 有外部语义 Watchdog，Freely 是进程看护

**Super-agent**：

- 云端状态 + 本地 daemon；外部 Watchdog Session 判断基础设施 + Worker 是否取得实质进展/方向偏离。
- effect 队列持久化；恢复提示先核对再重做。

**Freely**：

- supervisor/watchdog_sse/continuation/session resume；worktree 持久。
- `watchdog_sse` 是 SSE 路由，不是独立 LLM 判断；Manager 在 loop 内监督。
- 本地停止/机器离线即停。

**判定**：进程恢复 Freely 强；**语义 Watchdog 是 Freely 的缺口**。可做一个轻量“supervisor reviewer”定期看 Worker 进展，不必照搬云端。

### 4.8 上下文：DSH 管窗口，Freely 管长期文档

**Super-agent**：

- Inline/Spill、链式召回、前缀稳定；窗口是 cache。
- 适合单会话/跨 Thread 的短期上下文。

**Freely**：

- docs 是长期记忆（B1/B2/PRD/pre-tests/phase）；Worker 靠 skill 读。
- prompt 有 STABLE/SEMI/DYNAMIC 排序，但没有 manifest/校验；cache 多为估算。
- 跨会话/跨项目更久，但单会话窗口管理不如 DSH。

**判定**：**互补**。Freely 应保留 docs，补 prompt manifest/usage_reported；不需要把文档全塞窗口。

## 5. Freely 多出来的（不参与“谁更强”）

这些是 Freely 的 **code harness 交付能力**，Super-agent 没有对应：

- B1/B2 + SDD/TDD 规格/测试文档。
- 独立 Reviewer + 阶段评审 + PR 四问。
- PR/merge/closeout 门禁。
- worktree/test lane 隔离。
- 多项目 registry。
- ACP 多 harness 可替换。

这些不是“Super-agent 缺所以 Freely 赢”，而是 **Freely 的主意图本身更大**。比较时不能拿这些去要求 Super-agent，也不能因为 Super-agent 有 Router 就丢掉这些。

## 6. Super-agent 多出来的（不纳入 Freely 主意图）

- IM/Feishu 多渠道、个人助手场景。
- 云端/BYOM/多设备执行。
- 投机执行、异步 ReAct 全双工。
- 多客户端 panel。

这些可以作为未来补充，但不是 Freely 当前主意图的必要条件。**不要为了“像 Super-agent”而先做这些。**

## 7. 吸收清单（按主意图优先级）

| 优先级 | 吸收什么 | 映射到 Freely | 不吸收什么 |
| --- | --- | --- | --- |
| P0 | 讨论入口 + 事件级准入 | C-F：issue comment/PR review/CI → 事件；Fast gate 做来源/actor/幂等 | 不照搬完整 A2A/云端 Source |
| P0 | Thread/ownership/handback | C-B：followup_owners + handoff envelope + unread | 不做事件溯源重写 |
| P1 | Report 六态 + Attention | C-C：A2A report/attention 字段；单问题、目标会话 | 不做 Mandate 全量 |
| P1 | 批量路由 + 幂等 | Manager 批量决策；accept key | 不把 Manager 缩成纯 Router |
| P1 | prompt manifest + usage | C-C/context-cache：STABLE/SEMI/DYNAMIC + usage_reported | 不把 cache 当命中率 |
| P2 | 语义 Watchdog | 轻量 supervisor reviewer 看 Worker 进展/方向 | 不照搬云端 Watchdog |
| P2 | Assignment/Report 分离 | A2A task/executor 状态分离 | 不重写全部领域模型 |
| P3 | Harness 角色选择 | C-D：per-role slot + probe | 不先做 DSH adapter |

## 8. 评审结论

- **Super-agent 在“事件 → 准入 → 分派 → 交接 → 注意力”这一段明显更成熟**，尤其 Thread/Subscription、Report/Attention、ownership/handback、批处理、语义 Watchdog。
- **Freely 在“规格 → TDD → 独立评审 → 合并治理 → 多项目”这一段明显更强**，这是主意图，不应为了对比而削弱。
- **Freely 当前的真正问题不是“没有 Super-agent 的架构”，而是主意图里的讨论入口/交接/持久/约束还没有闭环。**
- 吸收原则：**只吸收重叠意图的运行时 primitive；不整体迁移领域模型；不为了像 Super-agent 而增加云端/IM/投机执行。**

## 9. 证据

- 智东西：https://www.zhidx.com/p/606311.html
- IT之家：https://m.ithome.com/html/1020615.htm
- 驱动中国：https://app.qudong.com/article/528135.html
- 原型：https://github.com/deepseek-ai/dsh-superagent-prototype @ 6337fc823ce20251c8de8085948165c81aaa701e
- 原型 `docs/000-008`、`prompts/`、`src/app/{tools,notices,prompts}.ts`、`src/executor/dsh.ts`
- Freely：`agents/*`、`a2a/*`、`task-lifecycle-scan.py`、`platform-adapter.py`、`run-acp-prompt.py`、`agent_working.py`
