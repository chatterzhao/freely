# Code Review: worktree guard
- issue_id: I-20260511T0731Z-A
## Implementation Decision Note
- decision: worktree_has_active_worker 检查 handoffs pending/launched + PID 存活验证
- why_this: 不用 DB 约束，运行时判断，PID 验证防止状态不准
