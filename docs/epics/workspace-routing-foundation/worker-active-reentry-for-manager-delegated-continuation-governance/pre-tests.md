# Pre-tests: worker-active-reentry-for-manager-delegated-continuation-governance

## Pre-merge acceptance

1. Active worker reentry from manager launch
- setup:
  - target worker 已有 active supervisor + active AI
  - manager continuity 指向该 worker prompt
- expect:
  - runtime 写入 delegated continuation intake
  - runtime 触发 `request_local_continuation_reentry`
  - runtime 不重复调用 `start_workcell_supervisor_async`

2. Existing launch linkage regression
- expect:
  - inactive worker 仍按原有路径被拉起

## Post-merge acceptance

1. 在 `develop` 用真实 Freely manager 再跑剩余 feature worktree 巡检
- expect:
  - manager 生成 worker handoff 后，worker 不再长期停留在 `pending_delegated_continuation_ids != none && last_consumed == none`
