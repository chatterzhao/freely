---
candidate_id: C-20260625T061044Z-A
status: promoted
source_raw: raw-20260625T061044Z
created_at: 2026-06-25
milestone: M-20260625T061044Z-A
---

## C-20260625T061044Z-A: issue-sync batch before daemon scan

- candidate_format_version: v2
- title: daemon start 时自动运行 issue-sync batch
- status: promoted
- decision_reason: 零 AI 消耗处理机械同步，大幅减少 Manager token
- next_action: 合并
- revisit_trigger: N/A
- acceptance_criteria:
  - daemon start 时在 scan 前运行 issue-sync batch
  - 输出记录到 daemon log
- promotion_gate: 功能正确
- promoted_issue_path: docs/issues/I-20260625T061044Z-A/issue.md
- milestone: M-20260625T061044Z-A
- session_refs: []
