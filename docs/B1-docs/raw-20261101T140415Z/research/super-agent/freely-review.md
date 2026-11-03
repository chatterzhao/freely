# Freely 现状评审：按意图，不按叫法

> 证据以 develop 为准；只读代码/文档，不把“测试绿”当成“runtime 已接线”。

## 总评

**设计方向：优秀。实现闭环：不足。**

Freely 的核心选择是对的：不把 ReAct 调度塞进 runtime，不让 DSH/Router 接管 loop；用 Manager/Worker/Reviewer + worktree + docs/DB + gates 承担生命周期。它比 Super-agent 更适合“项目所有者 + SDD/TDD + 独立评审 + 合并治理”。

但 Super-agent 真正强的“事件 → 准入 → 分派 → 交接 → 注意力”这一段，Freely 目前多数只做到**库/CLI/文档**，没有接进真实 runtime：

- 事件有 schema，没有生产 poller；
- ownership 有表，没有调用方；
- report 有 CLI，没有真实 patrol 对照；
- harness 有选择器，没有 session 生命周期；
- ReAct 有 session 并发，没有单 session 的 async job/steer/cancel 契约。

所以不是“设计差”，是“最后一公里没接”。

## 1. 注意力 / 多任务

**Super-agent 意图**：人的注意力只能盯 3–5 个 Session；系统要接管会话管理，人只看“需要我什么”。

**Freely 现状**：

- Manager 统一巡检/派工；多 worktree/多 Worker；`live-status`/`fleet-status`/scan/milestones。
- 但人仍要理解多个工位/分支/文档；没有一个聚合的“现在需要我”的面。
- 没有 Web Panel；CLI/文档是主界面。

**判断**：并发模型强于“单 Session”；注意力聚合弱于 Panel。Freely 的并发单位是 worktree/session，不是聊天 Session，这更适合项目交付，但也让人更难一眼看全。

**态度**：保持 worktree/session 并发；先做 CLI 聚合视图（needs_human/attention/gate/PR），不急于 Web Panel。

## 2. 跨信道连续性

**Super-agent 意图**：IM 方案 A、PR 改方案 B，Agent 统一记忆。

**Freely 现状**：

- docs/DB/worktree/A2A task 持久；issue/PR 评论入口有 C-F schema/adapter；IM 没接。
- C-F `discussion_events.collect()` 只读 `.freely/run/discussion-events.json`；生产没有 poller 写它。
- `platform-adapter` 有 `list_issue_comments/list_pr_reviews/list_ci_checks`，但无 runtime 调用方。

**判断**：文档/工单连续性强；跨信道事件连续性目前是“有 schema、无入口”。如果宣称“持续监控讨论”，现在是不成立的。

**态度**：改造后吸收。先接 GitHub issue comment/PR review/CI 的增量 poller → event store → scan/Manager；IM 另议。

## 3. 主动 / 事件准入

**Super-agent 意图**：事件驱动，Fast Path 程序过滤 + Slow Path LLM 判断；高噪音低触发率。

**Freely 现状**：

- `discussion_events.admit()` 有确定性准入：source 开关、bot、actor allowlist、addressed、strength。
- `task-lifecycle-scan` 汇总 `events.unread/by_source/latest`。
- 但没有平台 poller；scan 的 events 只是摘要，未形成“候选事件 → Manager 决策”的闭环。
- 事件 body 是外部不可信输入；C-F 没有强调 prompt injection/trust boundary。

**判断**：admission 规则是好的 primitive；真正缺的是来源接线和“摘要→行动”的转换。直接照搬 Super-agent 的 LLM Slow Path 会引入成本，可先规则+Manager 判断。

**态度**：吸收 Fast Path；Slow Path 先交给 Manager，不新建第二套 Router。

## 4. Thread / 订阅 / ownership

**Super-agent 意图**：同一 PR/IM 话题的后续事件直通 owner；多对多订阅；跨范围 handback 一次；不重复开单。

**Freely 现状**：

- `handoff_store.py` 有 `delegation_tasks/handoffs/handoff_messages`，支持 create/assign/followup/handback/stop/worker_died/reviewer_fail/append_message。
- 测试覆盖状态机；但 **生产 runtime 没有任何 `HandoffStore` 引用**（grep 仅 tests）。
- `agent_working._prompt_after_connect` 解决 new/fork 后首条 task message；但没有 owner 路由/handback 接入 Manager/Worker。
- A2A task 仍是单行状态，后续消息容易覆盖/丢。

**判断**：领域模型比现有 A2A task 干净，是正确的方向；但只在库里，等于 ownership 协议没生效。`test-handoff-e2e` 甚至断言 `messages==0`，不是真 E2E。

**态度**：改造后吸收，优先级最高。必须接 Manager/Worker 生命周期，不是再加表。

## 5. 上下文组织 / 长期记忆

**Super-agent 意图**：Inline & Spill + 链式召回；对象 ID 引用图；窗口是 cache。

**Freely 现状**：

- docs/DB/artifacts/PRD/pre-tests 长期存储强；`prompt_manifest` 记录 segment/prefix hash/usage 三态。
- 但 Manager 读哪些文档仍靠 prompt/人工选择；没有统一对象 ID/下一跳引用协议；没有链式召回。
- prompt manifest 是“记录”，不是“检索”。

**判断**：Freely 的长期文档比 Super-agent 的链式召回更结构化，但“按需展开”的能力弱；容易 prompt 过长或漏读。

**态度**：改造后吸收。先做 artifact 引用/摘要协议（PRD/pre-tests/verdict/evidence 的统一 ID + 下一跳），不急着上图数据库。

## 6. 异步 ReAct / 单 session 交互

**Super-agent 意图**：经典 ReAct 的 `run()` 阻塞、半双工；改成 `start()/stop()`，后台执行、前台继续接指令。

**Freely 现状**：

- ACP `session/prompt` 一次跑完；`run-acp-prompt.py` 没实现 model-level start/stop；没有 `session/cancel` 契约。
- `sse-watchdog.sh` 可向 Manager 注入 `session/prompt`；但这是 best-effort，未证明 in-flight 时是排队/打断/失败。
- 多个 Worker 是不同 session，互不阻塞；单 Worker 内长工具仍阻塞。
- `acp-bridge.py` 的 idle monitor 明确保护 in-flight prompt；没有取消路径。

**判断**：高层意图（人不被单 session 绑住）Freely 也解决了一部分，靠多 session/worktree + Manager 注入；单 session 内全双工没解决。Freely 不应该复制 ReAct runtime，但需要 harness 级 async job/steer/cancel 契约。

**态度**：暂缓实现，先实验。若证据表明长工具/中途改向是瓶颈，只补 HarnessPort async job/steer/cancel；不做全双工 ReAct runtime。

## 7. 多信道输出

**Super-agent 意图**：IM 低打扰 ≤100 词；GitHub/邮件结构化高密度；Router 统一对外。

**Freely 现状**：

- GitHub/Gitee issue/PR 评论；Manager 文档有回复规范；没有 IM/Feishu；没有统一 Router 对外层。
- 输出质量靠 agent prompt + review，不是 runtime 强制。

**判断**：GitHub 交付是强项；低打扰/统一语气/跨信道适配弱。Freely 的 Reviewer/gates 能补质量，但不能补信道适配。

**态度**：保持差异；先定义“对外消息契约”（长度/结构/谁回复），不急着接 IM。

## 8. 计算/状态/执行环境分离

**Super-agent 意图**：云端无状态 loop + Session DB + 端侧 daemon/BYOM，跨设备持久。

**Freely 现状**：本地 CLI/daemon + worktree + SQLite；执行环境就是本机；无云端控制面/daemon。

**判断**：这不是 Freely 当前主意图；引入云端会显著增加安全/运维/权限复杂度。本地 worktree 已经满足“环境不复制”。跨设备/BYOM 是未来形态，不是缺陷。

**态度**：不吸收（当前）。保持本地项目所有者模型；多设备另立 raw。

## 9. Watchdog

**Super-agent 意图**：主系统外独立 Control Loop；不仅进程存活，还判断 Worker 实质进展/方向偏离；Watchdog 本身是 Agent，可用自然语言询问/修正。

**Freely 现状**：supervisor heartbeat、`watchdog_sse.py`、continuation watchdog、Loop Guard L0–L3；偏进程/SSE/循环检测，不是语义进展判断；没有独立 Watchdog Agent。

**判断**：基础设施恢复 Freely 不弱；语义偏离/无效循环的独立判断弱。让 Watchdog 直接改主系统风险高，应先只读观察。

**态度**：改造后吸收（只读语义观察器），不直接把写权限交给 Watchdog。

## 10. 授权 / Mandate

**Super-agent 意图**：Source Policy + 准入表 + Mandate（版本/范围/强度）；谁能发起、工作范围多大。

**Freely 现状**：Constitution/Laws/gates/worktree/branch/B1/B2 是强项目治理；事件级准入只有 `discussion_events.admit`，无 Mandate 模型；C-B ownership 未接。

**判断**：Freely 的项目授权更强；事件级“谁能触发/范围多大”弱。不要复制完整 Mandate；需要事件准入 + 信任边界。

**态度**：保持项目治理；只吸收事件级 admission/trust boundary，不引入 Mandate 全量。

## 11. Report / Attention / 决策

**Super-agent 意图**：六态 report、单问题 attention、批量 accept/stop/ignore/unavailable、幂等。

**Freely 现状**：C-C `agent_protocol` + `a2a-report`/`a2a-decide`；Manager 文档要求使用；但真实 patrol 对照/自动批量路由未证明；pre-tests 有重复 `actual_output: pending`，gate 仍通过。

**判断**：schema/CLI 是正确 primitive；运行时强制/真实闭环不足，证据质量有瑕疵。

**态度**：吸收并补真实闭环；不新增平行模型。清理重复 pending 证据。

## 12. 可观测 / Panel

**Super-agent 意图**：Panel 只显示需要人的事；Overview/Source/Trigger/Eval/Execution/Settings。

**Freely 现状**：`live-status`/`fleet-status`/scan/milestones/progress；CLI/文档为主；无 Web Panel。

**判断**：对开发者够用；对“注意力瓶颈”不如 Panel。Freely 的用户是项目所有者/开发者，CLI 可接受；但缺少一个“现在需要我”的聚合。

**态度**：暂缓 Web Panel；先做 CLI 聚合视图，复用现有状态。

## 13. 实验/证明

**Super-agent 意图**：用消融/批处理实验证明架构，不是只讲理念。

**Freely 现状**：单测/gate 多；没有多任务调度 benchmark；没有“双层 vs 单 session”对照。

**判断**：Freely 的工程治理强，但架构主张缺少量化证据；不能用 Super-agent 的合成负载直接证明 Freely。

**态度**：补最小实验（真实 patrol 的前后对照、事件延迟、人工介入次数），不套用 300 条消息合成负载。
