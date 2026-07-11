## C-20260711T100936Z-A: rc=143 stop vs crash 分类

- candidate_format_version: v2
- title: daemon stop rc=143 与意外崩溃区分
- status: promoted
- decision_reason: 简单文件标记方案，monitor 检测 stop_marker 存在 → stop_requested → exit 0
- acceptance_criteria:
  - daemon stop → monitor 输出 stopReason=stop_requested, exit 0
  - AI crash → monitor 输出 stopReason=unknown, exit 1
- promotion_gate: 代码合并 + daemon 验证
- promoted_issue_id: I-20260711T100936Z-A
- milestone: M-20260711T100936Z-A
