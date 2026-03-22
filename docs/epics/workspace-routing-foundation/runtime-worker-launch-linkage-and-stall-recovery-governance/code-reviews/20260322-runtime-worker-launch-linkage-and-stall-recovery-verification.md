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
- real post-merge acceptance on `develop`
  - `manager-worker-launch-state.env` recorded all three launched worker prompt paths
  - `fleet-status` showed worker supervisors/AI active on the three target worktrees

## Residual risk

- manager continuity 里的 worker prompt 解析当前依赖 prompt 文件路径和 prompt 文本中的 `你的 worktree：` 结构，后续若 manager handoff 格式继续演化，应考虑把 handoff queue 进一步结构化
- worktree cleanup 尚未执行；当前 worktree 仍有未提交 closure writeback，且本地分支与 `develop` 已 `1 1` 分叉，因此本轮只能记为 `retained-with-reason`，不能判成 `verified-retirable`

## Cleanup evidence

- `git rev-list --left-right --count develop...HEAD` -> `0 1`
- `git diff-tree --no-commit-id --name-only -r HEAD` -> 当前分支唯一待吸收的 docs-only closure commit 仍只涉及 issue / progress / review / milestone 四个 runtime-worker-launch canonical 文档
- `git status --short` -> 当前 worktree 仅这四个 closure 文档为 modified；目标 issue 无新的 runtime implementation 改动
- `git ls-remote --heads origin feature/runtime-worker-launch-linkage-and-stall-recovery-20260322` -> no match
- `./bin/wt-status-all` -> `Summary: total=6, dirty=4`; 当前工位仍为 `DIRTY`，且其他 dirty 工位需按 ownership 显式跳过，因此尚未满足 cleanup lifecycle 的 `target clean`
