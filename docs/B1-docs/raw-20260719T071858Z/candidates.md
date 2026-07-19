---
candidate_id: C-20260719T071858Z-A
status: promoted
source_raw: raw-20260719T071858Z
created_at: '2026-07-19'
milestone: M-20260719T071858Z-A
---

## C-20260719T071858Z-A: Manager prompt 模板补 --role worker + a2a_task.py --role 改为 required

- candidate_format_version: v2
- title: Manager a2a-exit prompt 模板补 --role worker，a2a_task.py --role 移除危险默认值
- status: promoted
- decision_reason: 证据链完整——A2A DB 确认 agent_id=manager，prompt 模板 L15528 确认缺 --role worker，a2a_task.py L830 确认默认值=manager。Option B（模板+默认值）是唯一能从协议层消除 silent failure 的方案。
- next_action: B2 → dev（修改 freely L15528-15536 + a2a_task.py L830）→ test → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - Manager prompt 模板中 a2a-exit 模板含 --role worker
  - Manager prompt 模板中委派 Worker 示例含 --role worker
  - a2a_task.py --role 无默认值（或 required）
  - 全仓 a2a-exit 调用点均已显式传 --role
- promotion_gate: 模板修改 + a2a_task.py 修改 + 全仓调用点验证
- open_questions: []
- acceptance_reviews:
  - reviewer: self-review
  - mode: inline
  - summary: 根因通过 A2A DB 实际数据 + daemon 日志 + 源码追踪三层验证确认。修复方案最小可验证。
  - verdict: pass
- promoted_issue_id: I-20260719T071858Z-A
- promoted_issue_path: docs/B2-docs/a2a/task-role-required/raw-20260719T071858Z/issues/I-20260719T071858Z-A.md
- milestone: M-20260719T071858Z-A
- session_refs: []
