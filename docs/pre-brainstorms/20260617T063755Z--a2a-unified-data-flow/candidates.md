# Candidates

## C-20260617T063755Z-A: A2A Unified Data Flow

- candidate_format_version: v2
- title: 消除 _db_rpc 旁路 + 启用 SSE + SQLite 回归异步 WAL
- status: promoted
- decision_reason: 011030Z Phase A 目标架构未达标，6 个方法绕过 A2A Server 直连 SQLite，SSE 零实现
- next_action: B2_IBM → pr-create-guarded → pr-merge-guarded
- acceptance_criteria:
  - a2a_task.py 无 _db_rpc 调用（0 instances）
  - streaming=True, SSE endpoint 可用
  - 6 个方法通过 A2A Server 路由
- promotion_gate: 语法检查通过，diff 确认 2 files, 78+ 40-
- promoted_issue_path: docs/issues/I-20260617T063755Z-A/issue.md
- milestone: M-20260617T063755Z-A
