# Progress: manager-supervision-quiet-period-stall-signal-governance

- issue_id: `I-20260328-0335-A`
- title: Manager supervision quiet-period stall-signal governance
- issue_path: `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/issues/manager-supervision-quiet-period-stall-signal-governance.md`
- phase_state: `in_verification`
- runtime_state: `ready-for-merge-judgement`
- summary: `2026-03-28` 的 dogfood 现场已确认：`operator_stop_requested` 在当前案例里不是产品 stop 需求，而是 `runtime-stalled-ai-recovery -> local_continuation_reentry -> supervisor trap` 的外显事件。primary gap 是 manager delegated-supervision quiet-period 被当前 stall detector 过度近似成强 stall。

## Current findings

1. 这不是 `same-lane busy` 旧误判的残留 scope，而是更深一层的 manager heartbeat contract 问题。
2. 当前实现主要依赖 `cycle-*.log` / `prompt-*.txt` mtime 作为 delegated-supervision stall 证据，这对长监督轮次过粗。
3. runtime 已有 restart storm / process churn 的 signal-first precedent，可作为更低回归的设计参考。
4. delegated backlog / prompt inflation 是并行证据面，但不应阻塞 primary stall-signal owner 的 materialization。

## Implemented slice

1. 在 `runtime/freely` 中新增了 delegated-supervision quiet-period idle-safe helper：
   - `same-lane busy` 的旧 continuity suppress 逻辑保持不变；
   - 新增的 suppress 依据不是“任意 active worker”，而是 launch-state 中与当前 manager 已消费 worker prompt 对应、且仍 delegated-busy 的 active worker；
   - 若最新 continuity 已经暴露更强 stall 证据，例如 launchable worker prompt 或 stale runtime refs，仍保持 recovery。
2. 新增了 focused regression：
   - `test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
   - `test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`
   - `test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
3. 已复跑并通过的相关边界：
   - `test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
   - `test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`
   - `test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
   - `test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
   - `test-freely-manager-delegated-continuation-older-busy-continuity-recovers`
   - `test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
   - `test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`

## Verification notes

1. `bash -n docs/system/workspace/scripts/runtime/freely` 已通过。
2. `./bin/governance-check` 已通过，仅保留仓库既有的 10 条 legacy pre-brainstorm naming warnings。
3. 这轮 owner 验证不再把 restart-storm / observability rename 作为 blocking acceptance；它们保留为 follow-on 复核面，避免把最小行为修复和更广的信号语义改动混成一个补丁。

## Next slice

1. 做最后一轮 targeted review，确认 quiet-period helper 只消费与当前 launch-state 相关的 busy worker truth。
2. 若治理检查继续通过，就可以进入 merge judgement。
3. `operator_stop_requested` 的 observability 区分与 restart-storm 复核继续单列 follow-on，不与当前行为修复混补。
