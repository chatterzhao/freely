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

全量审计发现 **11 处**仍使用默认路径（无 base_tool 后缀），分布在两个文件：

### monitor-ai-acp.sh (4 处)
- Line 181: `_bridge_log` 硬编码 → 使用 `_bridge_log_file "$project" "$_base_tool"`
- Line 403: `_bridge_pid_file "$project"` → `"$project" "$_base_tool"`
- Line 427: bridge-dead PID 检查 → 同上
- Line 441: ping socket → `_bridge_socket "$project" "$_base_tool"`

### freely (7 处)
- Lines 18863/18904/18935/18965/18998: `_acp_bridge_socket "$project"` → `"$project" "$_base_tool"`
- Line 21527: `_acp_bridge_pid_file "$project"` → 同上
- Line 21535: cleanup socket → 同上

### 额外修复
- `_detect_acp_failure` 接受 base_tool 参数，传入 Layer 0/3 检测
- `main()` 提取 base_tool from `--tool` 参数，传给所有 bridge 函数
