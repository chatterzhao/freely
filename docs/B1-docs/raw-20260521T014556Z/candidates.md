# Candidates

## C-20260521T014556Z-A: Manager 委派结果即时反馈

- candidate_format_version: v2
- title: Manager prompt 注入 dispatch results section，消除委派结果信息 gap
- status: needs_research
- decision_reason: raw-20260521T014556Z (GitHub #1520) Manager 委派 Worker 后无即时反馈，导致 launch_failed/stale_pid/初始化超时时空等 15+ 轮。在 `append_manager_handoff_context_if_needed` 中增加"委派结果" section，Manager 下一轮即可看到 dispatch 结果并正确决策
- next_action: 确认代码中 Runtime handoff 保留 dispatch result 的精确字段；确认 `append_manager_handoff_context_if_needed` 插入点；产出 acceptance review → B2 materialize
- revisit_trigger: acceptance review 完成后进入 B2_IBM
- acceptance_criteria:
  - Manager prompt 在 "Worker 汇报" section 前展示上一轮所有 dispatch 结果
  - 每条 dispatch 结果包含：timestamp, worker file ID, status (launched/launch_failed/stale_pid), 错误原因（如失败）
  - Manager 下一轮能看到 dispatch 结果并做出正确决策（重试/跳过/修复）
  - 不影响已有 handoff DB schema 和写入逻辑
  - 不影响 Worker 汇报 section 的现有格式
- promotion_gate:
  - acceptance review 通过
  - 确认代码中 `append_manager_handoff_context_if_needed` 的精确调用位置
  - 确认 Runtime 提供 dispatch result 的时机和字段
  - 格式化逻辑覆盖空结果、大量 worker、错误信息截断等边界
- open_questions:
  - `append_manager_handoff_context_if_needed` 目前是否已在 Manager 看到 Worker 汇报之前调用？
  - Runtime 写 handoff 时是否已保留足够的 dispatch result 信息？还是需要额外写入？
  - 大量 Worker dispatch 时是否需要分页/摘要？
  - 已消费/已处理的 dispatch 结果是否应被过滤掉不再展示？
- acceptance_reviews: []
- promoted_issue_path: ""（待 promotion）
- milestone: M-20260521T014556Z-A
- session_refs:
  - tool: claude-code
  - session_id: "{{SESSION_ID}}"
  - jsonl_path: unavailable://claude-code 不暴露 jsonl 路径
  - role: brainstrom_lead
