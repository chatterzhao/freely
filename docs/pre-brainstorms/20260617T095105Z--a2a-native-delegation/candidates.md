# Candidates

## C-20260617T095105Z-A: A2A-Native Delegation

- candidate_format_version: v2
- title: 消除 CSV 委派中转 — A2A Task.message 承载完整任务内容
- status: promoted
- decision_reason: CSV 是 pre-A2A 时代的遗留方案,A2A 协议原生支持 Task.message 委派
- next_action: B2_IBM 设计 → dev 实现 → pr-merge-guarded
- acceptance_criteria:
  - a2a-exit 不再有 --workers 参数
  - Task.message 承载完整 Worker 指令内容
  - freely runtime 从 tasks/list 查询委派任务而非读 CSV
  - Worker 从 Task.message 获取任务内容
  - 消除 worker_prompts_csv 所有引用
- promotion_gate: 对标 Routa/JiuwenSwarm 的 A2A 委派模式
- promoted_issue_path: docs/issues/I-20260617T095105Z-A/issue.md
- milestone: M-20260617T095105Z-A
- session_refs: []
