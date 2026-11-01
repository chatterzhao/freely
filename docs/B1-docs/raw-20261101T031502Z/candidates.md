---
candidate_id: C-20261101T031502Z-A
status: promoted
source_raw: raw-20261101T031502Z
created_at: 2026-11-01
milestone: M-20261101T031502Z-A
---

# Candidates

## C-20261101T031502Z-A: Super-agent 对比研究与协作方向立项

- candidate_format_version: v2
- title: 交付 Super-agent 对比研究、概念全量对照与协作方向立项
- status: promoted
- decision_reason: 研究本身是一个有边界的交付：需要区分文章主张/原型实现/Freely 现状，逐项评估路由、交接、缓存与 harness 抽象，并把可推进方向登记为 candidate。它不实现任何候选，因此不能复用后续实现 issue 的载体。
- next_action: 合并 I-20261101T031502Z-A 并收口；四个 needs_research candidate 由后续独立 issue 承接。
- revisit_trigger: 若研究结论被新证据推翻（例如 DSH 发布带 ACP 的版本、或 Freely 已完成 HarnessPort），重开研究并更新结论。
- acceptance_criteria:
  - 研究覆盖七个比较维度与七处结构性差异
  - 概念全量对照覆盖领域对象、机制、运行时与观测面，并标出同名不同义
  - 两张 archify 对比图可打开、可读
  - 四个后续方向以 needs_research candidate 登记，带 next_action/revisit_trigger
  - `governance-merge-gate --range develop..HEAD` 通过
- promotion_gate: 研究文档 + 概念对照 + 两张图 + 四个 candidate 合并，门禁通过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 事实可回溯到原型 `docs/000-008`、`prompts/`、`src/app/tools/main.ts`、`src/app/notices.ts`、`src/app/prompts.ts`、`src/executor/dsh.ts` 与 Freely `agents/`、`a2a/`、`three-loop`、`run-acp-prompt.py`
  - verdict: pass
- promoted_issue_id: I-20261101T031502Z-A
- promoted_issue_path: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/issues/I-20261101T031502Z-A.md
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-B: 实现 follow-up ownership 与 handback

- candidate_format_version: v2
- title: 实现 Worker 对已完成工单后续线程的 follow-up ownership 与 handback
- status: needs_research
- decision_reason: Super-agent 用 `Subscription` + `followupOwners` + `handback` 把“同一 Thread 的后续消息归谁处理”做成运行时事实；Freely 的 Worker 没有平台线程订阅，PR/Issue 后续讨论只能经 Manager/A2A 或重新进入 intake，容易出现重复开单、漏接或上下文断档。新研究进一步确认 A2A task 行没有 message/owner 历史，且 new/fork 会丢 message。结论：需要 delegation/ownership 协议，不是给 task 行加字段。
- next_action: 协议 v0 已落 `handoff.md`（envelope/ownership/handback/幂等/超时）；下一步做五类后续消息行为盘点 + 真实 PR/issue 评论回放；通过 acceptance review 才 promote。
- revisit_trigger: 出现同一 PR/Issue 的后续评论被重复开单、被漏接，或 Manager 因中转 follow-up 出现上下文丢失/重复委派时，立即重启本 candidate；若连续两个里程碑未出现该类事件，可降级为观察项。
- acceptance_criteria:
  - 五类后续消息各自有明确的 owner 判定规则，且能回答“这条消息现在归谁”
  - 越界消息只能 handback 一次，并携带理由与目标工单，不产生重复任务
  - 已停止/已关闭工单不会被后续消息自动复活，除非满足显式条件
  - 协议草案给出幂等键与超时释放规则，可用 pre-tests 验证
- promotion_gate: 行为盘点完成 + 协议草案通过 Reviewer 审查 + 至少一个真实后续线程场景的端到端演练通过
- depends_on: C-20261101T031502Z-F
- open_questions:
  - follow-up ownership 应落在 A2A task 元数据还是独立的轻量账本
  - 线程订阅的边界是“同一 PR/Issue”还是“同一 raw issue 关联的所有线程”
  - 与人工 stop、wt-close 的优先级如何排序
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 新证据显示 Freely 的 A2A 是 task 行而非 message/artifact 历史，且首次 new/fork 交接会丢 message；缺口比原判断更深，尚未达到 promotion gate
  - verdict: needs_more_research
- promoted_issue_id: pending://C-20261101T031502Z-B
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-C: 实现类型化 report/attention 与 prompt 前缀契约

- candidate_format_version: v2
- title: 实现 Manager 的类型化 report/attention、批量路由与 prompt 前缀契约
- status: needs_research
- decision_reason: 逐项实现对比显示，DSH 在路由批处理、逐条拒绝、accept 幂等、六态 report、结构化 attention、稳定 relay key、Policy 置尾保护 prefix cache 上都有代码落点；Freely 的 Manager 同时承担 scan、派工、纠偏、收口与人工插话，缺少批量决策、类型化交接与显式 prompt 前缀契约。结论：按 P1 实现，不再停留在度量。
- next_action: 字段契约已在 `handoff.md` §6 起草；下一步补 prompt manifest（stable/semi/dynamic 段）与 cache/usage 基线，并做真实 patrol 前后对照；通过 acceptance review 后再实现。
- revisit_trigger: Manager 单轮上下文接近 rotation 阈值、同一轮处理超过 3 个工单导致漏派/错派、或 cache 命中率连续下降且 prompt_bytes 上升时，重启本 candidate；若度量显示路由开销占比很低，则降级为观察项。
- acceptance_criteria:
  - 给出 Manager 每轮 patrol 的上下文成本基线（字符/token/文档数）与 cache hit/miss 基线
  - 明确 Manager 可以读什么、不可以读什么，并有可检查的 prompt/skill 约束
  - 路由至少支持“批量决策 + 单条拒绝”，且拒绝原因可追溯
  - `report` 至少覆盖 progress/waiting/ready/blocked/failed/dropped 六态，`attention` 含问题、目标会话、所需动作
  - 交接 relay 有稳定幂等键；prompt 明确“稳定前缀 / 可变尾部”，并给出 cache 对照数据
- promotion_gate: 基线度量完成 + 协议/字段设计通过 Reviewer 审查 + 一个真实 patrol 周期的前后对照
- depends_on: C-20261101T031502Z-B
- open_questions:
  - 上下文成本以字符、token 还是文档数为口径
  - 六态 report 与现有 A2A state 如何映射而不破坏兼容
  - prompt 前缀契约由 runtime 还是 agent/skill 层强制
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: `runtime-contracts.md` 证明 Freely 已有 STABLE/SEMI/DYNAMIC 排序但无 manifest/校验，cache 仍多为估算；字段契约与基线未完成，不能 promote
  - verdict: needs_more_research
- promoted_issue_id: pending://C-20261101T031502Z-C
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-D: HarnessPort 与角色级 harness 选择（Freely 主应用）

- candidate_format_version: v2
- title: 实现 HarnessPort 与角色级 harness 选择（Freely 主应用）
- status: needs_research
- decision_reason: 三角色已经能通过 `agent-table.toml` 的 `{role}_slot` 分 harness，但缺少统一 HarnessPort、角色级配置/探测、UI/CLI/TUI 入口；DSH 不再作为 harness adapter（另立 C-E）。
- next_action: 先补 HarnessPort 接口草案 + RoleHarnessConfig 映射（`{role}_slot`、adapter 约束、model 缺口），再用 `harness-status` 做 per-role probe；通过 acceptance review 后再 promote。
- revisit_trigger: 新增 harness 需要改 runtime 多处、角色级选择出现静默降级，或 UI/CLI 开始各自写 `agent-table.toml` 时，立即重启本 candidate。
- acceptance_criteria:
  - HarnessPort 覆盖 probe、session 生命周期、prompt/resume/interrupt、usage/cache、工具与 skills
  - 三角色可分别选 harness；配置只写 `agent-table.toml` 的 `{role}_slot`
  - per-role probe 区分 native/degraded/unknown，缺失时 fail-closed
  - UI/CLI/TUI 共用同一 JSON 后端，不各自写文件
  - 明确 DSH 插件不在本 candidate；见 C-E
- promotion_gate: 接口草案 + RoleHarnessConfig 设计 + 至少一个非默认 harness 的 probe 证据 + acceptance review
- open_questions:
  - 是否引入 `{role}_adapter`，还是永远全 ACP
  - 角色级 model/effort 放 agent-table 还是 slot 配置
  - 运行中 Manager 轮换如何不打断当前 patrol
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: `harness-selection.md`/`harness-strategy.md` 给出角色级选择与配置落点，但接口/探测/UI 后端尚未定稿，不能 promote
  - verdict: needs_more_research
- promoted_issue_id: pending://C-20261101T031502Z-D
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-E: `@freely/dsh-freely` Freely-host 插件

- candidate_format_version: v2
- title: 实现 `@freely/dsh-freely`：Freely 保留 loop，DSH 只做 harness
- status: needs_research
- decision_reason: DSH 主插件可注入 `agents/sessionController/tools/skills/systemPrompt` 等服务，因此可以让 Freely 保留 Manager/Worker/Reviewer、A2A、scan、gates、worktree、PR，只把 harness 换成 DSH；这不是 ACP adapter，也不是 DSH-host 治理插件。
- next_action: 先做 P0/P1 spike：插件骨架 + bridge + Manager session；验证首次 `session.new` 能收到 task+role prompt、handoff 不丢、gate 能阻断；再决定是否 P2/P3。
- revisit_trigger: DSH 服务 API 不稳定、插件无法注入 session/tools/skills，或必须同时启用 DSH Router/Ticket 才能工作时，回到方案 C（不做）。
- acceptance_criteria:
  - 插件注入所需 DSH services，且不加载 `dsh-superagent`
  - Manager/Worker/Reviewer 使用独立 DSH preset/session
  - 首次 session 收到 task message + role prompt；handoff envelope append-only
  - 一个真实 issue 从 Manager 到 PR，全程无 ACP
  - gate exit code 能阻断；usage 能区分 reported/estimated
- promotion_gate: P0/P1 spike 通过 + 独立 acceptance review + 明确 DSH 服务 API 稳定性结论
- open_questions:
  - DSH 服务 API 是否对第三方插件稳定开放
  - 配置权威在 DSH settings 还是 `.freely/harness.toml`
  - DSH 单仓/单 host 下多项目怎么办
  - Python runtime 子进程生命周期如何管理
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 插件架构与 DSH service 注入面已有代码级依据，但尚无 spike；不能 promote
  - verdict: needs_more_research
- depends_on: C-20261101T031502Z-B, C-20261101T031502Z-D, C-20261101T031502Z-F
- promoted_issue_id: pending://C-20261101T031502Z-E
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-F: 讨论入口：issue comment / PR review / CI 进入 scan 或事件流

- candidate_format_version: v2
- title: 让 scan/事件流真正监控 issue 讨论、PR review 评论与 CI 结果
- status: needs_research
- decision_reason: 主意图明确要求 scan 持续监控 issue、issue 讨论、chat。当前 `task-lifecycle-scan.py` 只处理 open issue 与 body；`pull_raw_issue` 只写 body；`fetch_issue` 虽带 comments 但未被消费；PR review/CI 完全没有入口。这不是 ownership 问题，而是“事件根本没进来”。
- next_action: 先做来源盘点（issue body/issue comment/PR review comment/PR review/CI/chat）与事件 schema（source/event_id/thread_key/actor/body）；用真实 issue 评论与 PR review 回放，确认 scan/Manager 能看到；再决定走 scan 还是 DSH 式 Source/Trigger。
- revisit_trigger: 出现“人在 issue/PR 里回复了但 Freely 没反应”、同一讨论重复开单、或 CI 失败没有进入 Manager 时，立即重启本 candidate。
- acceptance_criteria:
  - 六类来源都有明确入口、event_id、thread_key、actor 与去重规则
  - issue comment/PR review 评论能进入 Manager 的 scan/queue，不需要人再开 chat
  - CI 结果能作为事件进入，不依赖人转述
  - 同一事件重复拉取不产生重复任务
- promotion_gate: 来源/事件 schema + 至少一个真实 issue 评论与一个 PR review 的回放 + acceptance review
- open_questions:
  - 入口放 scan 还是独立 Source/Trigger 层
  - 评论/评审是否要完整历史，还是只取增量
  - 平台 event id 与 thread_key 如何统一
  - 与现有 chat 入口的优先级/去重
- acceptance_reviews:
  - reviewer: session-self
  - mode: code-path review
  - summary: scan 无 comment 处理、pull 只写 body、PR review/CI 无入口；缺口成立，但没有回放证据
  - verdict: needs_more_research
- promoted_issue_id: pending://C-20261101T031502Z-F
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []
