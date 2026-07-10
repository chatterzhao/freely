---
candidate_id: C-20260710T110249Z-A
status: promoted
source_raw: raw-20260710T110249Z
created_at: 2026-07-10
milestone: M-20260710T110249Z-A
---

## C-20260710T110249Z-A: monitor-ai-acp.sh per-tool 命名同步

- candidate_format_version: v2
- title: monitor-ai-acp.sh 同步 per-tool bridge 命名
- status: promoted
- decision_reason: PR #3842/3849 引入 per-tool bridge 后，monitor-ai-acp.sh 的检测代码未同步更新，所有 bridge 级检测（idle、fatal、PID）都在检查不存在的默认路径。需同步命名并在修复后确认 rc=143 是否解决。
- next_action: B2 设计实现
- revisit_trigger: 如果 Option A 修复后 rc=143 仍然发生 → 需要深入追踪第三个 kill 路径
- acceptance_criteria:
  - _detect_acp_failure 使用 per-tool bridge log
  - bridge-dead PID 检查使用 per-tool PID file
  - _bridge_pid_file 和 _bridge_log_file 统一传入 base_tool
- promotion_gate: B1 预研完成
- open_questions:
  - 是否存在第三个 kill 路径（非 bridge 检测触发）
- acceptance_reviews: []
- promoted_issue_id: I-20260710T110249Z-A
- promoted_issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260710T110249Z/issues/I-20260710T110249Z-A.md
- milestone: M-20260710T110249Z-A
- session_refs: []

## 改动计划

### monitor-ai-acp.sh: 同步 per-tool 命名
- `_detect_acp_failure`: 接受 base_tool 参数，使用 per-tool bridge log
- `main()`: 提取 base_tool，传入 `_detect_acp_failure` 和 `_bridge_pid_file`
- `_bridge_pid_file "$project"` → `_bridge_pid_file "$project" "$_base_tool"`
- `_bridge_log_file "$project"` → `_bridge_log_file "$project" "$_base_tool"`
