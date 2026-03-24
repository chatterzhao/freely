# Pre-tests

## Pre-merge acceptance

1. stale `manager-worker-launch-state.env` 存在时，runtime 再次消费 latest continuity 会把 consumed continuity 更新到最新文件。
2. 若 latest continuity 派生出新的 worker prompt，runtime 会消费最新 prompt set，而不是停留在旧 prompt csv。
3. `ensure_manager_once` 在 manager supervisor 已运行时，仍会触发 latest continuity consumption。
4. `baseline-status` / `live-status` 能显示 latest continuity / prompt set 的 generated 与 consumed truth。

## Post-merge acceptance

1. 在 `develop` 上真实执行 `freely chat` 后，若主管产生新一轮 worker prompt set，worker 会切到最新 prompt set，而不是继续沿用更早 delegated continuation。
2. `ACTIVE_RUNNING_WORKER_COUNT` 只能作为 fleet-wide 观察信号；若其他 issue family / runtime-owned lane 仍在运行，它可以大于当前 issue family 的 same-round worker 数。不要把该值单独当成 `I-20260322-0445` reopen 的判据。
3. 对这条 issue family 的 canonical `develop` acceptance，重点检查的是 same-round latest continuity / worker prompt generated-consumed truth 是否一致，而不是要求 fleet-wide worker 总数在后续轮次保持某个固定值。
