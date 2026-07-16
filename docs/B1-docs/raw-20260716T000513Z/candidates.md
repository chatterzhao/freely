---
candidate_id: C-20260716T000513Z-A
status: promoted
source_raw: raw-20260716T000513Z
milestone: M-20260716T000513Z-A
---

## C-20260716T000513Z-A: fix agent_assign timing + worker contract

- candidate_format_version: v2
- title: move agent_assign to worker launch + auto-infer worker contract
- status: promoted
- decision_reason: agent_assign 移到 worker launch 入口确保时序正确；worker contract 从已有数据推断避免依赖 manager prompt
- next_action: B2→dev 实现
- acceptance_criteria:
  - worker launch 时 agent_assign 在 daemon 启动前写入 agent_working
  - worker daemon 通过 _resolve_current_agent_id 获取正确 role
  - worker contract 字段从现有数据自动推断
- promotion_gate: bash -n + daemon 测试 worker 启动
- promoted_issue_id: I-20260716T000513Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/issues/I-20260716T000513Z-A.md
- milestone: M-20260716T000513Z-A
