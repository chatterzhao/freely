# Candidates

## C-20260617T090408Z-A: Fix worker_prompts_csv dead loop

- candidate_format_version: v2
- title: FreelyAgentExecutor 持久化 worker_prompts_csv 等 Freely 特有字段
- status: promoted
- decision_reason: execute() 丢弃 worker_prompts_csv 导致 Manager delegate_workers 死循环
- next_action: B2_IBM → pr-create-guarded → pr-merge-guarded
- acceptance_criteria:
  - a2a-exit --workers 创建的任务在 DB 中有 worker_prompts_csv 字段
  - _db_exit_contract_field manager worker_prompts_csv 返回非空值
  - Manager delegate_workers 后 Worker ACP session 成功启动
- promotion_gate: 语法检查通过
- promoted_issue_path: docs/issues/I-20260617T090408Z-A/issue.md
- milestone: M-20260617T090408Z-A
