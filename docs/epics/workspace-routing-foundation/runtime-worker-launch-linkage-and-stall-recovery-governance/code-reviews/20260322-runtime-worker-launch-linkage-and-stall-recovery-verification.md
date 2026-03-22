# Code Review - runtime-worker-launch-linkage-and-stall-recovery-governance

- issue_id: `I-20260322-0245`
- result: `pass`

## Verified

1. manager handoff 不再只停在 worker prompt 文件
- `manager_runtime_launch_workers_from_latest_handoff()` 会读取最新 manager continuity 中的 worker prompt 路径
- 每个 prompt 会被转成目标 worker worktree 的 delegated continuation intake
- target worker worktree 会被写成 `DESIRED_RUNTIME_STATE=running` 并由 runtime 启动 supervisor

2. manager stalled AI recovery 已进入 runtime-owned 控制面
- `recover_stalled_manager_ai_if_needed()` 会在 `cycle log` 长时间不更新且有更新的 `intake.pending` 时触发
- 恢复优先走 graceful reentry，再重启 supervisor

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `./bin/governance-check`

## Residual risk

- manager continuity 里的 worker prompt 解析当前依赖 prompt 文件路径和 prompt 文本中的 `你的 worktree：` 结构，后续若 manager handoff 格式继续演化，应考虑把 handoff queue 进一步结构化
