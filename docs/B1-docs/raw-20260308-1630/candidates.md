# Candidates: 阶段前缀式进度标识

## C-20260308-1631

- title: 用阶段前缀式主进度标识替代 `in_progress` / `active`
- status: promoted
- decision_reason: 现有状态词无法从值本身看出阶段，必须依赖额外字段拼读；阶段前缀语法更适合 AI 路由和人类扫描。
- promoted_issue_path: `docs/B2-docs/ibm/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- acceptance_hint: 1) 定义 `phase_state=<prefix>_<stage>` 的唯一词典；2) 阶段前缀固定为 `todo/in/done/blocked`，`completed` 只用于 issue 生命周期终态；3) `done_ibm` 作为 IBM->dev handoff 真源，不采用 `ready_*` / `todo_for_*` / `pending_*`；4) `milestone_state` 收缩为队列归属；5) `runtime_state` 保持独立；6) skills 与 milestone policy 统一引用新词典和状态图。
- scope:
  - `docs/LAWS.md` 状态词典
  - `docs/milestones.md` 队列语义与阶段语义拆分
  - issue / progress / recovery 模板字段迁移
  - 核心 routing / IBM / dev-loop skills 判断逻辑
- impact: 中高 - 会改变现有执行态词典，但能显著降低状态歧义
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
