# Candidates

## C-20260514T103532Z-A: agent handoff protocol v2

- candidate_format_version: v2
- title: 设计 agent handoff protocol v2 — 字段语义、状态机、线程模型、消费语义
- status: completed
- decision_reason: #343 的 validator/launcher 断开暴露了 handoffs 表作为交接媒介的协议层缺失。parent_handoff_id 闲置、consumed_by 无用、无线程模型、WORKER_HANDOFF_INJECT 不完整——这些不是孤立 bug，而是协议设计不完整的症状
- next_action: 完成 B2_IBM materialize，产出 I-* issue 进入 dev-loop
- revisit_trigger: B2_IBM 完成后
- acceptance_criteria:
  - handoffs 表新增 previous_worker_handoff_id、last_activity_at 字段，均由 runtime 管理
  - 所有 Runtime 状态 UPDATE 加乐观锁 `WHERE status='<期望当前状态>'`
  - mark_stale 基于 `last_activity_at` 不活跃检测（非墙钟总运行时长）：log 更新/PID 存活/socket 心跳任一信号持续 → 不触发。Worker 慢但活跃不超时
  - AI 不再调用 handoff.py CLI，改为在回复末尾输出 ` ```handoff ` JSON 块，由 Runtime 解析写入（AI 只输出 7 个字段，Runtime 合并其余字段）
  - auto-consume 在 manager 新 handoff 创建时自动触发：消费当前 raw_key 下所有 status IN (completed,blocked,rejected) AND consumed_by='' 的 worker 记录
  - 修复 handoff 携带结构化字段（repair_target_role, repair_target_handoff_id, validation_errors_json），替代自然语言散文
  - 上下文注入分层：Manager 获得线程历史 + fleet + scan + 未消费 worker 列表；Worker 仅获得 Task + 结构化 HANDOFF_INJECT（handoff_id + parent + previous_worker + 前序 completion_summary 截断）
  - launcher 和 validator 合一为 consume_delegate_workers
  - worktree_has_active_worker 只查 launched 状态
  - 状态机文档化：6 status 值 + 10 合法转换 + 守卫条件 + 乐观锁
  - 旧 handoff.py update/insert 指令从 agent docs 删除
- promotion_gate: #343 四个 bug 在新的 protocol 实现后全部消除
- open_questions: []
- acceptance_reviews:
  - reviewer: "ai-agent"
    date: "2026-06-16"
    decision: promote
    rationale: >
      预研质量高（558 行 brainstorms.md），12 项 acceptance_criteria 全部明确定义，
      状态机、乐观锁、JSON 协议、上下文分层等核心设计细节完整。
      #343 的四个 bug 在新协议下结构上不再存在（promotion_gate 结构满足）。
      open_questions 为空，B2_IBM 已完全 materialize：
      PRD、pre-tests、tasks、code-reviews 均已完成（at docs/epics/agent-handoff-protocol/）。
      Issue I-20260514T103532Z-A phase_state=completed、platform_state=closed。
      无阻拦项，建议正式 promote。
    findings:
      - acceptance_criteria: 12 项全部定义清晰，brainstorms.md 有对应的详细设计说明
      - promotion_gate: "#343 四个 bug 在新协议下结构上不存在" — 设计确认，code-review 确认
      - open_questions: 空 — 所有问题在预研中已收敛
      - B2_IBM_materialization: 完整 — PRD/pre-tests/tasks/code-reviews 均存在
      - issue_state: I-20260514T103532Z-A phase_state=completed, platform_state=closed
      - milestone: M-20260514T103532Z-A status=completed, candidate 已标记为 promoted
- promoted_issue_path: docs/issues/I-20260514T103532Z-A/issue.md
- milestone: M-20260514T103532Z-A
- session_refs: []
