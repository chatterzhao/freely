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
- next_action: 合并 I-20261101T031502Z-A 并收口；三个 needs_research candidate 由后续独立 issue 承接。
- revisit_trigger: 若研究结论被新证据推翻（例如 DSH 发布带 ACP 的版本、或 Freely 已完成 HarnessPort），重开研究并更新结论。
- acceptance_criteria:
  - 研究覆盖七个比较维度与七处结构性差异
  - 概念全量对照覆盖领域对象、机制、运行时与观测面，并标出同名不同义
  - 两张 archify 对比图可打开、可读
  - 三个后续方向以 needs_research candidate 登记，带 next_action/revisit_trigger
  - `governance-merge-gate --range develop..HEAD` 通过
- promotion_gate: 研究文档 + 概念对照 + 两张图 + 三个 candidate 合并，门禁通过
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

## C-20261101T031502Z-B: 已完成工单的 follow-up ownership 与 handback 协议

- candidate_format_version: v2
- title: 定义 Worker 对已完成工单后续线程的 follow-up ownership 与 handback 协议
- status: needs_research
- decision_reason: Super-agent 用 `Subscription` + `followupOwners` + `handback` 把“同一 Thread 的后续消息归谁处理”做成运行时事实；Freely 的 Worker 没有平台线程订阅，PR/Issue 后续讨论只能经 Manager/A2A 或重新进入 intake，容易出现重复开单、漏接或上下文断档。该缺口在 agent 协作层，且已被 `concept-map.md` 逐条确认，不是叫法差异。
- next_action: 先做行为盘点（不改代码）：枚举 PR comment、review、CI、issue comment、chat 插话五类后续消息当前落到 scan 还是 intake；定义 owner 判定、handback 结构、幂等键、超时释放与人工 stop 的优先级；产出协议草案与 pre-tests 设计，再决定是否进入 B2。
- revisit_trigger: 出现同一 PR/Issue 的后续评论被重复开单、被漏接，或 Manager 因中转 follow-up 出现上下文丢失/重复委派时，立即重启本 candidate；若连续两个里程碑未出现该类事件，可降级为观察项。
- acceptance_criteria:
  - 五类后续消息各自有明确的 owner 判定规则，且能回答“这条消息现在归谁”
  - 越界消息只能 handback 一次，并携带理由与目标工单，不产生重复任务
  - 已停止/已关闭工单不会被后续消息自动复活，除非满足显式条件
  - 协议草案给出幂等键与超时释放规则，可用 pre-tests 验证
- promotion_gate: 行为盘点完成 + 协议草案通过 Reviewer 审查 + 至少一个真实后续线程场景的端到端演练通过
- open_questions:
  - follow-up ownership 应落在 A2A task 元数据还是独立的轻量账本
  - 线程订阅的边界是“同一 PR/Issue”还是“同一 raw issue 关联的所有线程”
  - 与人工 stop、wt-close 的优先级如何排序
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 基于 Super-agent `002/003`、`prompts/subscriptions.md` 与 Freely `a2a/*`、`agents/*`、`scan-lifecycle-design.md` 对照，确认缺口真实存在
  - verdict: pass
- promoted_issue_id: pending://C-20261101T031502Z-B
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-C: Manager 路由/交接质量与 prompt/cache 契约

- candidate_format_version: v2
- title: 度量并约束 Manager 的路由/交接成本，建立类型化 report/attention 与 prompt 前缀契约
- status: needs_research
- decision_reason: 逐项实现对比显示，DSH 在路由批处理、逐条拒绝、accept 幂等、六态 report、结构化 attention、稳定 relay key、Policy 置尾保护 prefix cache 上都有代码落点；Freely 的 Manager 同时承担 scan、派工、纠偏、收口与人工插话，缺少批量决策、类型化交接与显式 prompt 前缀契约，长期是单点瓶颈。
- next_action: 先度量（不改代码）：统计 Manager 每轮 patrol 注入的 scan/A2A/文档引用体积、读实现的次数、转为 Worker 的指令比例、`[CACHE]` 命中率与 prompt_bytes；再设计批量路由/逐条拒绝、`report` 六态与 `attention` 字段、稳定 relay key、prompt 稳定前缀/可变尾部；用度量与对照数据决定改 prompt/skill 还是改 runtime。
- revisit_trigger: Manager 单轮上下文接近 rotation 阈值、同一轮处理超过 3 个工单导致漏派/错派、或 cache 命中率连续下降且 prompt_bytes 上升时，重启本 candidate；若度量显示路由开销占比很低，则降级为观察项。
- acceptance_criteria:
  - 给出 Manager 每轮 patrol 的上下文成本基线（字符/token/文档数）与 cache hit/miss 基线
  - 明确 Manager 可以读什么、不可以读什么，并有可检查的 prompt/skill 约束
  - 路由至少支持“批量决策 + 单条拒绝”，且拒绝原因可追溯
  - `report` 至少覆盖 progress/waiting/ready/blocked/failed/dropped 六态，`attention` 含问题、目标会话、所需动作
  - 交接 relay 有稳定幂等键；prompt 明确“稳定前缀 / 可变尾部”，并给出 cache 对照数据
- promotion_gate: 基线度量完成 + 协议/字段设计通过 Reviewer 审查 + 一个真实 patrol 周期的前后对照
- open_questions:
  - 上下文成本以字符、token 还是文档数为口径
  - 六态 report 与现有 A2A state 如何映射而不破坏兼容
  - prompt 前缀契约由 runtime 还是 agent/skill 层强制
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 基于 DSH `src/app/tools/main.ts`、`src/app/notices.ts`、`src/app/prompts.ts` 与 Freely `agents/manager-agent.md`、`three-loop`、`run-acp-prompt.py` 对照，确认实现级差距成立
  - verdict: pass
- promoted_issue_id: pending://C-20261101T031502Z-C
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-D: 把 agent harness 抽象为可切换基座（HarnessPort）

- candidate_format_version: v2
- title: 定义 HarnessPort，把 agent harness 变成可探测、可降级、可按角色选择的基座，并划清 DSH adapter/插件边界
- status: needs_research
- decision_reason: Freely 今天通过 ACP 适配多 CLI，但契约是隐式的：session/fork/resume、工具策略、skills、usage/cache 的差异靠代码分支兜底；DSH 原型没有 ACP 服务端，只有 Cordis 插件面，且 `engines.dsh` 钉版本。要把 harness 当可切换基座，必须先有显式能力契约；要让 DSH 成为其中一个基座，必须写 adapter，而不是加一个配置项。
- next_action: 先做能力盘点（不改代码）：列出当前 ACP adapter 对 Claude/Codex/OpenCode/Cline 的 session/fork/resume、stream、interrupt、tools、skills、usage/cache 支持矩阵；定义 HarnessPort 接口（probe、start、prompt、resume/fork、interrupt、usage、capabilities）与 per-role 选择/fallback；做 DSH adapter 可行性 spike（Cordis in-process vs 子进程桥）；给出“一个 loop 一个 owner”的插件边界。
- revisit_trigger: 新增第二个 harness 需要修改 runtime 多处、出现 harness 能力差异导致的静默失败、或团队要求把 gates/worktree 外溢成 DSH 插件时，立即重启本 candidate。
- acceptance_criteria:
  - 产出一张 ACP CLI 能力矩阵，标注“有/无/降级/需探测”
  - HarnessPort 接口覆盖 probe、session 生命周期、prompt/stream、interrupt、usage/cache、工具与 skills 能力
  - 支持按角色（Manager/Worker/Reviewer）选择 harness，并有 capability probe 与 fallback
  - DSH adapter 有可行性结论（in-process/子进程、session 映射、工具/权限、cache 语义）
  - 明确 DSH 插件只做 gates/worktree/issue 工具外溢，不再起 Router/Ticket
- promotion_gate: 能力矩阵 + 接口草案通过 Reviewer 审查 + 至少一个非 ACP 基座的 spike 结论 + 插件边界评审通过
- open_questions:
  - DSH adapter 走 Cordis in-process 还是子进程桥，哪个可维护性更好
  - 按角色选 harness 的最小配置面是什么，是否要暴露到 CLI/TUI
  - cache/usage 语义在不同 harness 间如何统一，缺失时如何标注
  - 插件外溢时，授权与状态所有权归谁
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 基于 DSH `package.json`/`cordis.patch.yml`（Cordis bundle、无 ACP）与 Freely `run-acp-prompt.py`、`session-lifecycle-protocol.md`、`AGENT_AI_TOOL` 配置对照，确认“基座可切换”需要显式端口而非配置开关
  - verdict: pass
- promoted_issue_id: pending://C-20261101T031502Z-D
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []
