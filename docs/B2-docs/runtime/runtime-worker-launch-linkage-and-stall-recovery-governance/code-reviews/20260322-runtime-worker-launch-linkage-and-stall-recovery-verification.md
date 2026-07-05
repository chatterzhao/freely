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
- worktree cleanup 尚未执行；即使当前 canonical closure writeback 固化后工位会恢复 clean，本地分支相对 `develop` 仍保留未吸收的 docs-only closure commits，因此本轮只能记为 `retained-with-reason`，不能判成 `verified-retirable`

## Cleanup evidence

- `git rev-list --left-right --count develop...HEAD` -> 当前分支仍领先 `develop`
- `git log --oneline --left-right develop...HEAD` -> 当前本地待吸收提交均为 docs-only closure commits
- `git diff-tree --no-commit-id --name-only -r HEAD` -> 最新本地 closure commit 仍只涉及 issue / progress / review / milestone 四个 runtime-worker-launch canonical 文档
- `git status --short` -> 固化本轮 closure writeback 前仅剩 issue / progress / review / milestone 四个 canonical 文档；目标 issue 无新的 runtime implementation 改动
- `git ls-remote --heads origin feature/runtime-worker-launch-linkage-and-stall-recovery-20260322` -> no match
- `./bin/wt-status-all` -> 当前工位在固化本轮 closure writeback 后会恢复 `CLEAN`；其余 dirty 工位仍需按 ownership 显式跳过，因此当前 cleanup blocker 仍是 develop absorption 与 project-level skipped dirty evidence
