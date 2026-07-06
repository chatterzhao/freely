---
candidate_id: C-20260703T114618Z-A
status: absorbed
absorbed_into: I-20260703T114618Z-A
source_raw: raw-20260703T114618Z18Z
milestone: M-20260703T114618Z-A
---

## C-20260703T114618Z-A: legacy issue

- candidate_format_version: v2
- title: 在 _persist_session_anchor_early() 中按 role 写入 agent_working session 记录
- status: absorbed
absorbed_into: I-20260703T114618Z-A
- decision_reason: _persist_session_anchor_early() 是每个 AI cycle 的锚点，此时 session_id 已确定。已有写入 session-state.env + session-store 的逻辑，添加 agent_working 写入只需一行 RPC。
- accepted_criteria:
  - daemon 启动后首个 AI cycle 即写入 agent_working.__manager__（带 session_id）
  - restart 后 agent_working 中有 manager session_id → 可 resume
  - worker/reviewer 的写入不受影响（已在 watchdog_sse.py 中正确实现）
- absorbed_into: I-20260703T114618Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260703T114618Z-A/issue.md
- milestone: M-20260703T114618Z-A
