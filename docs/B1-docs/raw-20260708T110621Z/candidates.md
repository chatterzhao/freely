---
candidate_id: C-20260708T110621Z-A
status: promoted
source_raw: raw-20260708T110621Z
milestone: M-20260708T110621Z-A
---
## C-20260708T110621Z-A: SSE 500 + pool + observability
- status: promoted
- decision_reason: StreamingResponse for SSE + agent-table pool read + stderr capture
- promoted_issue_id: I-20260708T110621Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T110621Z/issues/I-20260708T110621Z-A.md
- promotion_gate: /tasks/stream 返回 200 + pool 显示正确数字
- acceptance_criteria:
  - SSE /tasks/stream 返回 200 text/event-stream
  - pool 显示 agent-table.toml 中配置的值
  - A2A server stderr 被捕获
