# Pre-tests

## Pre-merge acceptance

1. stale `manager-worker-launch-state.env` 存在时，runtime 再次消费 latest continuity 会把 consumed continuity 更新到最新文件。
2. 若 latest continuity 派生出新的 worker prompt，runtime 会消费最新 prompt set，而不是停留在旧 prompt csv。
3. `ensure_manager_once` 在 manager supervisor 已运行时，仍会触发 latest continuity consumption。
4. `baseline-status` / `live-status` 能显示 latest continuity / prompt set 的 generated 与 consumed truth。

## Post-merge acceptance

1. 在 `develop` 上真实执行 `freely chat` 后，若主管产生新一轮 worker prompt set，worker 会切到最新 prompt set，而不是继续沿用更早 delegated continuation。
