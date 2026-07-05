---
candidate_id: C-20260627T084545Z-A
status: promoted
source_raw: raw-20260627T084545Z
created_at: 2026-06-27
milestone: M-20260627T084545Z-A
---

## C-20260627T084545Z-A: legacy issue

- candidate_format_version: v2
- title: a2a_tasks agent_id 改具体编号 + 字段补全
- status: promoted
- decision_reason: 全局替换风险可控（6 文件 ~15 处），一次性解决
- next_action: B2_IBM → dev → pr-merge
- revisit_trigger: N/A
- acceptance_criteria:
  - a2a_tasks insert 时 agent_id 存 worker_01 等具体编号
  - 所有查询兼容 LIKE 'worker_%' / LIKE 'manager_%'
  - worker_pid 写入非空
  - delivery_status 正确更新
- promotion_gate: freely daemon 启动后 a2a_tasks 新记录 agent_id 为具体编号
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: 审查 6 文件 15 处改动
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260627T084545Z-A/issue.md
- milestone: M-20260627T084545Z-A
- session_refs: []
