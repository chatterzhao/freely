---
candidate_id: C-20260627T121248Z-A
status: promoted
source_raw: raw-20260627T121248Z
created_at: 2026-06-27
milestone: M-20260627T121248Z-A
---

## C-20260627T121248Z-A: a2a worker_pid + manager check 修复

- candidate_format_version: v2
- title: a2a worker_pid + manager check 修复
- status: promoted
- decision_reason: WT2 遗留的 insert 端和 a2a_server 端缺口
- next_action: B2_IBM → dev → pr-merge
- acceptance_criteria:
  - freely insert 传 --worker-pid
  - a2a_server agent_id == "manager" → startswith("manager")
- promotion_gate: 新任务 worker_pid 非空，manager 查询兼容具体编号
- promoted_issue_path: docs/issues/I-20260627T121248Z-A/issue.md
- milestone: M-20260627T121248Z-A
