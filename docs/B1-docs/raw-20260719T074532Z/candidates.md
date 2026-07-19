---
candidate_id: C-20260719T074532Z-A
status: promoted
source_raw: raw-20260719T074532Z
created_at: '2026-07-19'
milestone: M-20260719T074532Z-A
---

## C-20260719T074532Z-A: a2a task + agent_working 使用真实 agent 实例 ID

- candidate_format_version: v2
- title: 接上 agent-table.toml pool 实例分配 → agent_working → a2a_tasks 的完整链路
- status: promoted
- decision_reason: DB 层（next_free / upsert / next_free_and_assign）和 Python 层（agent_working.py）已正确实现。断点全部在 shell 层（4处）和 prompt 层（1处）。Option B 全线修复。
- next_action: B2 → dev（修 freely L6064 + a2a_task.py --agent-instance + Runtime LIKE + prompt 模板）
- revisit_trigger: N/A
- acceptance_criteria:
  - agent_working.worker_id 在委派后非 NULL（格式: worker_NN:session_id）
  - a2a_tasks.agent_id 为具体实例（如 worker_03）而非 role 字符串
  - Runtime worker 发现可匹配 LIKE 'worker_%'
  - Manager prompt 含 agent_next_free 调用指令
- promotion_gate: 修复后 daemon 重启，Manager 委派 Worker → agent_working + a2a_tasks 均使用实例 ID
- open_questions: []
- acceptance_reviews:
  - reviewer: self-review
  - mode: inline
  - summary: 7层追踪，DB+Python 已正确，断点在 shell+prompt。5处修复分布在3个文件。
  - verdict: pass
- promoted_issue_id: I-20260719T074532Z-A
- promoted_issue_path: docs/B2-docs/{epic-name}/{story-name}/raw-20260719T074532Z/issues/I-20260719T074532Z-A.md
- milestone: M-20260719T074532Z-A
- session_refs: []
