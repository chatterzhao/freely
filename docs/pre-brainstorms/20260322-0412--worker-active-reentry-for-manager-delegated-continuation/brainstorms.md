# 预研：worker active reentry for manager-delegated continuation

## Why now

真实狗粮显示：`develop` 上的主管已经能生成稳定的 worker handoff，并且 runtime 也能把 handoff 转成目标 worker worktree 的 delegated intake 与 supervisor 启动。但当目标 worker 本来就有 active AI 时，这条 delegated continuation 不会被当前轮次及时消费。

结果是：
- manager 侧看起来已经完成了委派；
- worker 侧也显示 `ai_active`；
- 但 `pending_delegated_continuation_ids` 持续堆积，`last_consumed_delegated_continuation_ids` 不更新；
- git/worktree 生命周期因此继续悬空。

这不是 `I-20260321-1706` 的旧问题。那条线只覆盖 `operator_stop` 后通过 `chat` 重新拉起 worker；当前问题是 worker 已经活着，但 manager 新委派来的 delegated continuation 没有触发正确的 local reentry。

## Observed truth

1. `develop` 的主管当前已经把剩余 feature worktree 作为 worker 拉起。
2. 至少 `feature/three-loop-dev-loop-ai-native-definition-20260321` 与 `feature/cli-first-observability-surfaces-20260322` 都存在：
   - `intake_active_items: 1`
   - `status=delegated`
   - `classification=continuation`
   - `activity_state: ai_active`
3. 但其中至少两个 worker 的：
   - `pending_delegated_continuation_ids` 非空
   - `last_consumed_delegated_continuation_ids` 仍是 `none`

## Existing truth source boundary

- `I-20260321-1706` 已 completed，且验收口径是 “stopped worker + chat -> runtime reactivation”。
- `I-20260322-0245` 已覆盖 manager handoff -> worker launch linkage，以及 manager stalled AI recovery。
- 当前缺的是第三段：

`manager delegated handoff -> active worker local reentry -> delegated continuation consumed`

## Desired behavior

当 manager runtime 把 worker prompt 转成目标 worker intake 时：

1. 若目标 worker 没有 active supervisor/AI：
   - 继续走现有的 bootstrap + start supervisor。
2. 若目标 worker 已经有 active AI：
   - 不应只写 delegated intake 然后什么都不做；
   - 应显式触发本地 continuation reentry；
   - 让下一轮 prompt 把新 delegated continuation 吸收进去；
   - 保持同一个 worker workcell，不额外起第二个主循环。

## Candidate direction

- 在 manager->worker launch linkage 处补一层：
  - 目标 worker 已 active 时，直接 `request_local_continuation_reentry(target, intake_id)`
- 不把它做成新的 manager 逻辑或新工具抽象；
- 继续收敛到 runtime / watchdog 控制面。

## Acceptance hint

最小验收应是真跑：

1. manager continuity 生成 worker prompt；
2. target worker 预先存在 active AI；
3. runtime 处理 handoff 后：
   - target worker 不会再额外启动第二个 supervisor；
   - 但会触发 local continuation reentry；
   - 新 delegated continuation 最终进入下一轮 prompt / consumed evidence。
