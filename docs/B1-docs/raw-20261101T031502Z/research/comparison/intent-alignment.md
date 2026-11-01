---
analysis_id: INTENT-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 主意图对齐评审：Freely 的实现是否真的在解决它声称的问题

## 0. 主意图（以用户表述为准）

> Freely 是一个 **LLM(AI) 主动、自主、持久、连续的 code harness**。LLM 通过 **scan 持续监控 issue、issue 讨论、freely chat 插话讨论**，遵循 **项目意图、宪法、法律、门禁、tool、skill、MCP**，自己维护好 **规格文档和测试文档**，然后遵循 **SDD（规格驱动开发）、TDD（测试驱动开发）** 持续项目开发。

把它拆成可检查的八条：

1. **主动**：不等指令，持续发现值得做的事。
2. **自主**：自己决定下一步、派工、执行、收口。
3. **持久**：长期在线，异常/重启后能恢复。
4. **连续**：跨 issue/讨论/chat/PR 保持同一项目上下文。
5. **入口**：scan 真的监控 issue、issue 讨论、chat。
6. **约束**：遵循 intent/constitution/laws/gates/tool/skill/MCP。
7. **文档**：自己维护规格文档和测试文档。
8. **方法**：SDD + TDD 持续开发。

判断标准：**先看是否服务主意图，再看实现是否真的解决问题。** 与主意图冲突的机制，即使“先进”，也是拖后腿。

## 1. 三篇解读的差异

| 维度 | 智东西 | IT之家 | 驱动中国 |
| --- | --- | --- | --- |
| 定位 | 最完整，系统/成本/实验细节 | 中等，四特征/五模块/实验摘要 | 最概览，产品叙事 |
| 双层 | Router 可轻量、可不全是 LLM；批处理 | Router/Worker 分工 | 同 |
| 事件 | Fast/Slow 两级过滤、订阅直通、Inline/Spill、链式召回、投机执行 | 两级过滤、订阅、上下文机制 | 事件驱动、订阅直通 |
| 交互 | 异步 ReAct、IM 100 词、异步信道 | 异步 ReAct、信道定制 | 异步 ReAct |
| 持久 | 存算分离、BYOM、外部 Watchdog | 同 | 同 |
| 实验 | p50/p95、直通省 37% token、batch 6.4→1.6s | p50/p95、Router 压力 | 无 |
| 开放问题 | Router 扩展、长程记忆、A2A、安全 | 同 | 未展开 |

共同意图：

- 人的注意力是瓶颈，系统层要接管 Session 调度/上下文。
- 一个 Agent 跨渠道连续，但底层可以有多个隔离 Worker。
- 主动来自环境事件，不是人逐条 prompt。
- 持久来自状态/计算/环境分离 + 外部 Watchdog。
- Super-agent 是架构，不是产品；原型只实现子集。

差异带来的判断：

- 智东西最强调“系统层/成本/批处理”，说明 Router 不必是重 LLM；Freely 的 Manager 也应尽量轻，不要每轮读全量文档。
- IT之家/驱动中国更强调产品体验；不能把“多 Agent”当成目的。
- 智东西明确把 **A2A 列为开放问题**；Freely 现在用 A2A 做内部交接，是超前尝试，但必须自己补协议，不能假设 A2A 已解决。

## 2. 逐条对齐

| 主意图 | Freely 现状 | 判定 |
| --- | --- | --- |
| 主动 | Manager patrol + scan + auto-loop；scan 是轮询，不是事件订阅 | **部分实现**：能主动，但发现范围/时延受 scan 限制 |
| 自主 | Manager 派工、Worker 执行、Reviewer 审查、gates 收口 | **部分实现**：角色齐，但交接有丢消息/覆盖问题 |
| 持久 | supervisor/watchdog/continuation/session resume | **部分实现**：进程/会话可恢复；缺语义 Watchdog；本地离线即停 |
| 连续 | docs 长期记忆、session resume、worktree | **部分实现**：跨会话有文档；跨 issue 讨论/PR 线程不连续 |
| scan issue | 扫描 open issue，拉 body | **部分实现**：issue body 有，讨论 comment 没有进入 scan |
| scan 讨论 | 无 comment/thread 订阅 | **未实现**：issue/PR 后续讨论没有 owner，容易漏接 |
| scan chat | `freely chat` → `chats` 表 → Manager prompt | **已实现**：但靠 Manager 二次路由，不直达 Worker |
| 遵循 intent | Manager 启动参数给 intent 路径；prompt 把 intent 列入需求池 | **部分实现**：给路径，不等于每轮读/校验 |
| 遵循 constitution/laws | 通过 `constitution-guard`/`laws-enforcer` skill 预检 | **部分实现**：流程约束，未自动注入/强制 |
| 遵循 gates | IBM/TDD/PR/merge/wt-close gates | **已实现**：但有门禁漂移与 fail-closed 问题 |
| 遵循 tool/skill | 角色定义 + skills + commands | **已实现**：tool/skill 是主路径 |
| 遵循 MCP | ACP 会话传 `mcpServers: []` | **未实现**：Freely 不编排 MCP，取决于外部 CLI |
| 维护规格文档 | B1/B2 产出 PRD/pre-tests/tasks/code-review | **部分实现**：有文档，但可后补、无 schema、易漂移 |
| 维护测试文档 | pre-tests + test evidence + test-gate | **部分实现**：GREEN 硬、RED 软、全 not_applicable 仅 skill 约束 |
| SDD | B1/B2 + PRD + gates | **部分实现**：门禁在 PR/merge 检查，不是每步自动生成/校验 |
| TDD | RED skill + GREEN gate + test-pre-merge | **部分实现**：终态硬，过程软 |
| code harness | ACP 多 CLI + worktree + roles | **已实现**：但 per-role adapter 仍全局，DSH 不是 ACP |

## 3. 做得好的地方（应保留）

1. **角色分工与主意图一致**：Manager 不写代码，Worker 执行，Reviewer 独立审查；这比“一个 Agent 全干”更接近项目所有者。
2. **SDD/TDD 文档链**：B1/B2/PRD/pre-tests/tasks/code-review 是可审计的交付合同；DSH 没有这一层。
3. **门禁与证据**：测试/评审/PR/merge 有硬检查；不是“agent 说完成”。
4. **worktree/test lane 隔离**：符合多任务并行与环境隔离，不是纯 prompt 约束。
5. **harness 能力探针**：`harness-status` 区分 native/degraded/estimated，是 HarnessPort 的正确起点。
6. **文档作为长期记忆**：跨 session/跨天比 DSH 的单会话更久。
7. **多项目 registry**：有真实项目登记，不是单仓假设。

## 4. 有意图但实现没解决问题（缺陷）

### 4.1 scan 没有真正监控讨论

- `task-lifecycle-scan.py` 没有 comment/discussion 处理。
- `platform-adapter.fetch_issue` 虽然带 comments，但 `pull_raw_issue` 只写 issue body；scan 不用 comments。
- PR review comment/CI 没有进入 runtime。
- 结果：主意图里的“issue 讨论/PR 讨论”实际上没有闭环；Worker/Reviewer 的后续讨论靠人再开 chat/issue。

**判定：直接违背主意图，是最高优先级缺陷。**

### 4.2 交接把 Task/消息/执行者压成一行

- `a2a_tasks` 只有一条 `message`；Manager/Worker/Reviewer 覆盖同一行。
- `acp_session_connect` 在 `session/new|fork` 不发送 message；首次 Reviewer/死亡 Worker 反馈会丢。
- Reviewer 契约矛盾（禁止 a2a-exit vs 要求 a2a-exit vs JSON verdict）。

**判定：自主/连续被实现缺陷拖住；不是补充，是拖后腿。**

### 4.3 持久只有“进程看护”，缺语义 Watchdog

- Freely 有 supervisor/watchdog_sse/continuation，但 `watchdog_sse` 是 SSE 路由器，不是独立 LLM Watchdog。
- 没有“判断 Worker 是否取得实质进展/方向是否偏离”的外部模型回路。
- 本地 runtime 停止/机器离线即停，没有云端/远程执行。

**判定：部分实现；语义 Watchdog 是主意图“持久/自主”的补充，不是必须照搬云端。**

### 4.4 连续被“文档多源 + 线程无 owner”削弱

- phase_state 多写者、I-* 双解析、scan station/next_action 不一致。
- issue/PR 后续消息没有 owner；chat 只进 Manager prompt。
- 文档是长期记忆，但运行时并不自动把 PRD/pre-tests 注入 Worker；靠 skill 读。

**判定：文档链是优势，但“连续”仍靠纪律，不是运行时事实。**

### 4.5 约束是“路径 + skill”，不是“每轮校验”

- Manager 启动只传 intent/constitution 路径；LAWS 通过 skill 预检，不是自动注入。
- MCP 完全不编排。
- 门禁在 PR/merge 强，过程中弱。

**判定：部分实现；需要区分“必须硬注入的主意图/宪法”与“可按需读的法律/skill”。**

### 4.6 SDD/TDD 的门禁位置偏后

- B1/B2 文档在 PR/merge 检查；实现可以先写、文档后补。
- TDD 的 RED 是 skill 流程，GREEN/pretests gate 是终态；全 not_applicable 只由 skill 约束。
- 历史 pre-tests 431 份中 327 份有 not_applicable、247 份无 test_command（含旧 schema）。

**判定：方向对，但“持续 SDD/TDD”还没有变成每一步的运行时事实。**

## 5. 补充还是拖后腿

| 机制 | 判定 | 理由 |
| --- | --- | --- |
| B1/B2 + PRD/pre-tests | 补充 | 服务 SDD/TDD，是主意图的合同 |
| 独立 Reviewer | 补充 | 服务质量，不违背自主 |
| gates/worktree/test lane | 补充 | 让自主可交付、可审计 |
| 多项目 registry | 补充 | 扩展主意图，不是替代 |
| A2A task 行 | 拖后腿（当前实现） | 覆盖消息、丢交接、伪造 A2A |
| scan 只看 issue body | 拖后腿 | 直接漏掉“讨论” |
| 全局 adapter | 拖后腿（角色级选择） | 三角色不能真正分 harness |
| MCP `[]` | 未实现 | 主意图明确提到 MCP |
| 语义 Watchdog | 缺补充 | 持久/自主的恢复面 |
| DSH 插件 | 可选补充 | 不先服务主意图时，容易分散 |
| 过度文档/门禁 | 需平衡 | 对 tiny task 过重；不是原则错误，是适用范围 |

## 6. 主意图优先级

1. **先把“讨论入口”补齐**：issue comment/PR review/CI 进入 scan 或事件总线；否则“持续监控讨论”是假的。
2. **再修交接**：new/fork 发 message、角色 prompt、Reviewer 契约、handoff envelope/ownership。
3. **再谈 harness 选择**：角色级 slot 选择 + probe；这是主意图的“code harness”部分，但不能先于 1/2。
4. **最后才做 DSH 插件**：B2 是可选形态；如果 1/2 没解决，插件只会把缺陷带进 DSH。
5. **语义 Watchdog / 投机执行 / 异步 ReAct**：按需要补，不要为了“像 Super-agent”而堆。

## 7. 结论

**Freely 的主意图是对的，而且比 Super-agent 更接近“项目所有者 + SDD/TDD 交付”。** 但当前实现只完成了“角色 + 文档 + 门禁 + worktree”的骨架；主意图里最关键的 **讨论监控、消息级交接、语义恢复、MCP/约束注入、逐步 SDD/TDD** 还没有真正闭环。

所以不能简单说“Freely 机制优秀”。准确判断是：

- **意图层优秀**：SDD/TDD/Reviewer/gates 是差异化，不应丢。
- **实现层部分不合格**：scan 讨论入口、A2A 交接、Reviewer 契约、MCP、语义 Watchdog 是缺口。
- **补充层有价值**：B1/B2、worktree、test lane、harness probe 应保留。
- **拖后腿层要修**：A2A task 行、scan 只看 body、全局 adapter、无 owner 的讨论。

下一步按 B1 candidate readiness matrix 继续 research loop；上述 1/2 未闭合前，不进入 DSH 插件全量实现。
