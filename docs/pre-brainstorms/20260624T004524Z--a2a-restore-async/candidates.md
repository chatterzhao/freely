# Candidates

## C-20260624T004524Z-A: A2A server _restore_tasks 异步化

- candidate_format_version: v2
- title: A2A server _restore_tasks 后台线程化，消除启动超时
- status: promoted
- decision_reason: __init__ 同步阻塞导致 socket 延迟绑定 → health check 超时。改为 daemon 线程最简单安全。
- next_action: pr-create → pr-review → pr-merge → wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - _restore_tasks 不再在 __init__ 中同步调用
  - server socket 在恢复完成前即可接受连接
  - health check 超时消息不再误导 "may be TCP-only"
- promotion_gate: 代码修改完成 + 逻辑审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: review a2a_server.py _restore_tasks 异步化安全性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T004524Z-A/issue.md
- milestone: M-20260624T004524Z-A
- session_refs: []
