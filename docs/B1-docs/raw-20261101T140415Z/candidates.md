---
candidate_id: C-20261101T140415Z-A
status: promoted
source_raw: raw-20261101T140415Z
created_at: 2026-11-02
milestone: M-20261101T140415Z-A
---

# Candidates

## C-20261101T140415Z-A: 交接运行时 P0 修复（首条消息 + 存活判定）

- candidate_format_version: v2
- title: 修复跨工具/resume 失败交接的首条消息丢失，并把 agent 存活判定从 pgrep 换成 session/ping
- status: promoted
- decision_reason: `agent_working._do_new` 引用未定义变量（`message`、`sys`），跨工具或 resume 失败时必抛；`watchdog_sse` 不捕获该异常，SSE 断线且不重放，交接静默丢失。上游 `_check_agent_liveness` 用 `pgrep -f session_id` 误判 DEAD 并清空绑定，进一步把交接推入该路径。两个缺陷串联，是“反复交接时好时坏”的直接原因。
- next_action: B2 物化 `I-20261101T140415Z-A`；先写 RED 测试复现两条路径，再修实现。
- revisit_trigger: 若跨工具交接与 resume 失败路径在生产中不再出现，且 `live-status` 连续两个里程碑无 `agent_dead` 误报，可关闭本 candidate。
- acceptance_criteria:
  - `_do_new` 不再引用未定义名称；`session/new`、`resume` 失败回退、跨工具三条路径都能把首条 handoff 消息送达新会话
  - 新会话收到的首条消息包含 `[role:<role>]` 标记，worker 与 reviewer 两种角色都可验证
  - 存活判定改为 ACP `session/ping`；ping 成功不标 DEAD，ping 失败 fail-closed（只标记恢复，不发明会话）
  - 回归测试覆盖：`_do_new` 路径、ping 成功/失败、live session 不被清绑定
  - 不改 A2A 状态枚举、CLI 参数与 `agent-table` 语义
- promotion_gate: RED→GREEN 回归测试 + 现有 handoff/a2a 测试全绿 + `governance-merge-gate --range develop..HEAD` 通过
- open_questions:
  - `session/ping` 在 ACP bridge 不可达时应算 DEAD 还是 UNKNOWN（当前倾向 UNKNOWN，交给恢复流程）
  - 首条消息是否需要同时落 `messages_json`（当前 `_prompt_after_connect` 只发 prompt，不写消息历史）
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 代码路径已核对：`agent_working.py:223-232`、`watchdog_sse.py:120-140/450`、`a2a_server.py:598`（内存 Queue 不重放）；两个缺陷可在单测中稳定复现
  - verdict: pass
- promoted_issue_id: I-20261101T140415Z-A
- promoted_issue_path: docs/B2-docs/a2a/handoff/raw-20261101T140415Z/issues/I-20261101T140415Z-A.md
- milestone: M-20261101T140415Z-A
- session_refs: []

## C-20261101T140415Z-B: 交接信封与持久投递（outbox + owner）

- candidate_format_version: v2
- title: 为交接引入固定信封、持久 outbox、单 owner 与回执
- status: needs_research
- decision_reason: 即使修掉 P0 缺陷，交接仍是“写库 + 内存 SSE + 自由文本”，没有重试、没有顺序、没有“投递未达”状态；席位复用也让 owner 不稳定。Super-agent 的 `worker_report/worker_attention` + `delivery/relay/notice/reply` + `Ticket` 自持 session 是可借鉴的运行时件。
- next_action: 在 B2 里先定三件事：信封字段（工单卡/原始引用/≤600 字摘要/单问题）、outbox 状态机（pending/sent/failed + seq + attempts）、owner 规则（assignment 而非席位）；再决定是否进入实现。
- revisit_trigger: 出现“同一交接被投递两次/丢失无法定位”“接收方需要重新查库才能知道发生了什么”“同一 raw 的消息落到不同席位”中任意一条，即启动。
- acceptance_criteria:
  - 信封有固定字段，原始 Trigger 引用不被改写；问题只允许一个
  - outbox 三态可见，同工单+会话保序，失败退避且连续三次上健康项
  - owner 由 assignment 决定，席位只提供容量；handback 一次且可判定 `queued:false`
  - 至少一条真实交接链路的端到端回放
- promotion_gate: 信封/outbox/owner 三份设计 + 回放证据 + 独立 acceptance review
- open_questions:
  - outbox 与现有 `a2a_tasks.messages_json` 的关系（新表还是复用）
  - `worker_NN` 席位与 assignment 的绑定粒度
  - 是否把 `notice`（不唤醒）与 `relay`（唤醒）分开
- acceptance_reviews: []
- promoted_issue_id: ''
- milestone: M-20261101T140415Z-A
- session_refs: []
