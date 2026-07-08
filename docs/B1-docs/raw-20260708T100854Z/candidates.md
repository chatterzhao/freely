---
candidate_id: C-20260708T100854Z-A
status: promoted
source_raw: raw-20260708T100854Z
milestone: M-20260708T100854Z-A
---
## C-20260708T100854Z-A: A2A socket 路径统一 + 日志时间戳
- status: promoted
- decision_reason: 修复 freely shell `_a2a_socket_path` 加 .sock + watchdog 日志加时间戳
- promoted_issue_id: I-20260708T100854Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T100854Z/issues/I-20260708T100854Z-A.md
- promotion_gate: `_a2a_socket_path` 返回带 .sock 的路径 + watchdog 日志有时间戳 + daemon 重启后 SSE 连接成功
- acceptance_criteria:
  - `_a2a_socket_path` 返回路径与 server/client 一致（带 .sock）
  - watchdog-sse.log 每行带时间戳
  - daemon 启动后 `-S "$_a2a_socket"` 检查通过
  - SSE watchdog 能连接到 A2A server
