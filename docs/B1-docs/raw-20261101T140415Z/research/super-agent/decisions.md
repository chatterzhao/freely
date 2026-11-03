# 吸收/改造/暂缓/不吸收：ADR

> 判断标准：是否服务 Freely 主意图（项目所有者 + SDD/TDD + 独立评审 + 合并治理），是否只增加运行时 primitive 而不引入第二套调度权，是否有真实证据/可验证闭环。
>
> 状态：`accepted`（决定做）、`proposed`（建议做，待 B1/B2）、`deferred`（暂缓，有触发条件）、`rejected`（当前不做）。

## D1. 事件入口：吸收，但先接 GitHub，不建新 Source 层

- status: accepted
- intent: issue comment / PR review / CI 能进入 scan/Manager，而不是只看 issue body。
- decision: 在现有 `platform-adapter` + `discussion_events` 上补增量 poller；scan 消费 event store；不新建独立 Source/Trigger 服务。
- why: C-F 已有 schema、准入、适配器方法；缺的只是生产 poller 和 scan 行动化。新建 Source 层会与 scan 双入口。
- what not: 不做 webhook、不做 IM/Feishu、不做完整事件溯源。
- evidence: `discussion_events.py`、`platform-adapter.py:list_issue_comments/list_pr_reviews/list_ci_checks`、`task-lifecycle-scan.py:events`。
- next: B1 candidate「C-F runtime wiring」；先 GitHub，真实 fixture 回放。

## D2. Thread/ownership：吸收，优先级最高

- status: accepted
- intent: 同一 PR/Issue 的后续消息归 owner；跨范围 handback 一次；new/fork 不丢消息；不重复开单。
- decision: 把 `handoff_store` 接入 Manager/Worker 生命周期；A2A task 双写兼容；后续消息按 thread_key/owner 路由。
- why: 领域模型已经写好，但生产零调用；仅给 A2A task 加字段会继续覆盖/丢消息。
- what not: 不做完整 A2A RPC/事件溯源；不另建第二套 Task 表。
- evidence: `handoff_store.py`、`agent_working.py:_prompt_after_connect`、grep 显示 runtime 无 HandoffStore 调用。
- next: B1 candidate「C-B runtime wiring」；真实 #4070 线程回放 + stop/worker death/Reviewer 3 轮。

## D3. Report/Attention/批量决策：吸收并强制闭环

- status: accepted
- intent: 六态 report、单问题 attention、批量 accept/stop/ignore/unavailable、幂等。
- decision: 保留 `agent_protocol` + `a2a-report`/`a2a-decide`；Manager 每轮真实使用；补一次真实 patrol 前后对照；清理 pre-tests 重复 pending。
- why: schema/CLI 已有；Manager 文档已要求；缺真实 patrol 证据与自动批量路由。
- what not: 不把 Manager 缩成纯 Router；不做完整 Mandate。
- evidence: `agent_protocol.py`、`manager-agent.md:179-181`、C-C pre-tests 双 `actual_output`。
- next: B1 candidate「C-C patrol proof」；usage/cache 三态 + 事件→决策延迟。

## D4. 上下文组织：改造后吸收，先做引用协议

- status: proposed
- intent: 窗口当 cache；Inline & Spill；按需链式召回。
- decision: 先统一 artifact 引用（PRD/pre-tests/verdict/evidence/issue/PR 的稳定 ID + 摘要 + 下一跳），不建图数据库；prompt 仍由 Manager/Worker 按引用读取。
- why: Freely 长期文档强，但 Manager 读什么靠人工；直接做链式召回图会过度设计。
- what not: 不把全部历史塞 prompt；不做跨月记忆系统。
- evidence: `prompt_manifest.py` 只记录 manifest，不负责检索；docs/PRD/pre-tests 已有稳定路径。
- next: B1 candidate「artifact reference protocol」，先用 Markdown/JSON 索引验证。

## D5. 异步 ReAct：暂缓，先实验；只补 HarnessPort async job/steer/cancel

- status: deferred
- intent: 长工具不阻塞会话；执行中可接新指令/改向/取消。
- decision: 不在 Freely core 实现 ReAct runtime；先测 ACP in-flight `session/prompt` 语义、长工具阻塞、人工介入；有证据再补 harness 能力。
- why: 高层意图已由多 session/worktree + Manager 注入部分解决；全双工 ReAct 会引入第二套调度/并发状态；Freely 主意图不需要个人助手级全双工。
- what not: 不复制 DSH `start()/stop()` 到 Freely runtime；不把 ReAct 当 runtime 状态机。
- evidence: `run-acp-prompt.py` 无 start/stop；`acp-bridge.py` idle monitor 保护 in-flight；`sse-watchdog.sh` best-effort 注入；无 `session/cancel`。
- trigger: 长工具 P95 阻塞造成交付延迟；执行中改向只能等/杀进程；Manager 误判 Worker 卡死。
- next: B1 experiment「Harness async capability」，产出 ACP 行为矩阵；必要时再 candidate。

## D6. Router/Worker 双层：保持差异，不新增 Router

- status: rejected (as literal adoption)
- intent: 连续性与吞吐量分开。
- decision: 保留 Manager/Worker/Reviewer；Manager 已承担全局协调，Worker 隔离执行；不新增常驻 Router Session，不把 Manager 缩成 Router。
- why: 再加 Router 会形成第三层/双 loop；Freely 的 Manager 还承担 scan/建工位/收口，不能只路由。
- what not: 不照搬单 Router 批处理作为新组件。
- evidence: `manager-agent.md`、`a2a_task.py`、worktree 并发。
- next: 只借鉴“批量决策/幂等”，已在 D3；不新 Router。

## D7. 多信道输出：保持 GitHub 强项，IM 暂缓

- status: deferred
- intent: IM 低打扰 ≤100 词；GitHub/邮件结构化；统一对外。
- decision: 先把 GitHub/Gitee issue/PR 输出契约固化；不接 IM/Feishu；不新建统一 Router 回复层。
- why: Freely 用户是项目所有者/开发者，GitHub 是主界面；IM 接入是另一条产品线。
- what not: 不为了“像 Super-agent”接 IM。
- evidence: `platform-adapter.py`、Manager 文档；无 IM adapter。
- next: 若接 IM，另立 raw；先定义消息长度/结构/谁回复。

## D8. 云端无状态 loop + 端侧 daemon/BYOM：当前不吸收

- status: rejected
- intent: 跨设备持久在线；执行环境不复制。
- decision: 保持本地 CLI/daemon + worktree + SQLite；不做云端控制面/端侧 daemon。
- why: 与 Freely 本地项目所有者模型冲突；安全/运维/权限复杂度高；当前 worktree 已满足环境不复制。
- what not: 不做 BYOM/多设备执行。
- evidence: 本地 runtime/worktree；无 cloud/daemon。
- next: 多设备需求出现时另立 raw，不在本架构研究里做。

## D9. 语义 Watchdog：改造后吸收，只读观察

- status: proposed
- intent: 不只进程存活，还判断 Worker 实质进展/方向偏离；外部 Control Loop。
- decision: 做只读语义观察器（读 report/events/diff/gate），输出 attention/建议；不直接改主系统/提示词/规则。
- why: Freely 已有进程/SSE/continuation watchdog；缺语义判断；直接给写权限风险高。
- what not: 不做“Watchdog 自动改主系统”。
- evidence: `watchdog_sse.py`、continuation/Loop Guard；无独立语义 Watchdog。
- next: B1 candidate「semantic watchdog read-only」；先影子运行，不阻断。

## D10. Mandate/Policy：保持项目治理，只吸收事件级准入

- status: rejected (full model) / accepted (admission subset)
- intent: 谁能发起工作、范围多大、策略版本。
- decision: 保留 Constitution/Laws/gates/worktree 授权；事件级只做 source/actor/addressed/strength 的准入与信任边界；不引入完整 Mandate。
- why: Freely 的项目治理更强；完整 Mandate 会把事件驱动领域模型搬进来，超出主意图。
- what not: 不做 Cross-Source identity mapping/Policy version/Mandate 全量。
- evidence: `discussion_events.admit`、治理文档、gates。
- next: 在 D1 内补“评论是不可信输入”的边界。

## D11. Panel：暂缓，先 CLI 聚合

- status: deferred
- intent: 人一眼看到“现在需要我什么”。
- decision: 先做 CLI/JSON 聚合（needs_human/attention/gate/PR/阻塞），不做 Web Panel。
- why: 用户是开发者；CLI 足够；Panel 是独立产品面。
- what not: 不做 6-tab Web UI。
- evidence: `live-status`/`fleet-status`/scan/milestones。
- next: 若 CLI 聚合仍不够，再立 Panel raw。

## D12. 跨实例 A2A：暂缓

- status: deferred
- intent: 组织内/组织间多实例、权限边界隔离后的协作。
- decision: 不做跨实例协议；先保证单项目/多 raw 内的 A2A task 正确。
- why: 主意图当前是单项目/团队；A2A 是开放问题。
- what not: 不为了架构图造跨实例协议。
- evidence: `a2a_server.py`/`a2a_task.py` 是单项目 task 状态。
- next: 多实例需求出现再研究。

## D13. 投机执行：当前不吸收

- status: rejected
- intent: 讨论未定时后台先做，值得才交付。
- decision: 不在 Freely 做 speculative execution；先保证授权/证据/gate 的确定性。
- why: 与“只做被授权工作/证据可追溯”冲突；成本/丢弃/权限复杂；主意图不需要。
- what not: 不后台自动开 PR/改代码。
- evidence: 无对应；B1 预研是“先研究再承诺”，不是投机。
- next: 不做；若未来做，必须单独授权/审计。

## D14. 实验：补最小真实对照

- status: accepted
- intent: 用证据证明架构，而不是只讲理念。
- decision: 补三组最小实验：事件入口延迟/去重；一次真实 patrol 前后对照（usage/cache/人工介入）；长工具阻塞/改向行为。
- why: Freely 没有调度 benchmark；Super-agent 的合成负载不能直接外推。
- what not: 不套用 300 条消息合成负载当结论。
- evidence: 现有 tests 多为单测/gate；无 benchmark。
- next: B1 experiment，产出数据后再决定 D5/D9。

## 优先级

1. **D2 ownership runtime**（没有它，讨论入口也没有归属）
2. **D1 event ingress**（没有它，主动性是假的）
3. **D3 report/attention 闭环**（让 Manager 决策可审计）
4. **D14 实验**（为 D5/D9 提供证据）
5. D4 引用协议、D9 语义 watchdog（按需）
6. 其余保持差异/不吸收

## 明确不做的

- 全双工 ReAct runtime、投机执行、云端/BYOM、完整 Mandate、Web Panel、跨实例 A2A。
- 不是因为“Super-agent 不好”，而是因为它们不服务 Freely 当前主意图，且会引入第二套调度/权限/运维复杂度。
