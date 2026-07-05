- issue_id: I-20260505T1210Z-A-B
- issue_path: docs/B2-docs/ibm/issue-state-refactor/issues/I-20260505T1210Z-A-B.md

# code-review: issue-sync platform_state fix

## Implementation Decision Note

- decision: issue-sync cmd_close 只写 platform_state=closed，cmd_create 写 platform_state=open，cmd_promote 写 phase_state=absorbed
- why_this: 消除跨层污染——issue-sync 作为本地→平台桥，只应管理平台层字段
- alternatives_considered: 在 cmd_close 中判断 kind 再决定写 status 或 phase_state——拒绝，职责不清
- boundary_non_goals: promote/comment/update 逻辑不变
- residual_risk: 被 issue-sync 污染的 raw（status=closed）需手动恢复为 phase_state=absorbed

## Changes reviewed
- bin/issue-sync cmd_close line 540: status→platform_state
- bin/issue-sync cmd_create line 424: +platform_state open
- bin/issue-sync cmd_promote line 626: status→phase_state

## Decision: Approve
