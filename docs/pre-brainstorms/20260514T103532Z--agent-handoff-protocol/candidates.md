# Candidates

## C-20260514T103532Z-A: agent handoff protocol v2

- candidate_format_version: v2
- title: 设计 agent handoff protocol v2 — 字段语义、状态机、线程模型、消费语义
- status: proposed
- decision_reason: #343 的 validator/launcher 断开暴露了 handoffs 表作为交接媒介的协议层缺失。parent_handoff_id 闲置、consumed_by 无用、无线程模型、WORKER_HANDOFF_INJECT 不完整——这些不是孤立 bug，而是协议设计不完整的症状
- next_action: 完成 B2_IBM materialize，产出 I-* issue 进入 dev-loop
- revisit_trigger: B2_IBM 完成后
- acceptance_criteria:
  - handoffs 表新增 previous_worker_handoff_id 字段，raw_key 作为隐式 thread_id（不新增独立字段）
  - parent_handoff_id 和 previous_worker_handoff_id 均由 runtime 在 insert 时写入（不再依赖 AI）
  - consumed_by 在 manager 创建新 handoff 时由 runtime 自动标记（所有 unconsumed worker 批量消费）
  - WORKER_HANDOFF_INJECT 注入完整上下文（PARENT_HANDOFF_ID、PREVIOUS_WORKER_HANDOFF_ID + 上一轮 worker 的 completion_summary/evidence_paths、同 raw_key 线程历史摘要）
  - AI 不再调用 handoff.py CLI，改为在回复末尾输出 ` ```handoff ` JSON 块，由 Runtime 解析写入
  - AI 只输出它负责的 7 个字段（exit_kind, reason, restart_point, next_action, completion_summary, evidence_paths, worker_prompts_csv），Runtime 合并其余 18 个字段
  - launcher 和 validator 合一为 consume_delegate_workers 函数
  - worktree_has_active_worker 只查 launched 状态
  - 旧 handoff.py update/insert 指令从 agent docs 中删除
  - 状态机文档化：6 个 status 值，10 个合法转换，每个有守卫条件
- promotion_gate: #343 四个 bug 在新的 protocol 实现后全部消除
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: ""
- milestone: ""
- session_refs: []
