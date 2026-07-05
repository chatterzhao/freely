# Candidates
## C-20260511T073100Z-A: legacy issue
- title: worktree 有活跃 worker 时拒绝新分配
- status: promoted
- decision_reason: 同工位无并发防护，worktree 有活跃 worker 时新分配会覆盖，需 PID 检查
- promoted_issue_path: docs/issues/I-20260511T073100Z-A/issue.md
- milestone: M-20260511T073100Z-A
- completion_note: I-20260511T073100Z-A 已完成 closeout，worktree 并发防护已吸收到 develop
