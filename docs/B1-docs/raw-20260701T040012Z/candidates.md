---
candidate_id: C-20260701T040012Z-A
status: promoted
source_raw: raw-20260701T040012Z12Z
created_at: 2026-07-01
milestone: M-20260701T040012Z-A
---

## C-20260701T040012Z-A: legacy issue

- candidate_format_version: v2
- title: 将 A2A 健康检查从 socket 轮询改为日志检测
- status: promoted
- decision_reason: socket 检查不可靠，log-based 用 A2A 自己输出的就绪信号
- next_action: B2 → dev → test → PR
- acceptance_criteria:
  - Daemon 启动时 A2A 健康检查在 15s 内通过
- promotion_gate: daemon start 不再出现 A2A timeout 警告
- open_questions: []
- promoted_issue_id: I-20260701T040012Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260701T040012Z-A/issue.md
- milestone: M-20260701T040012Z-A
- session_refs: []
