# Progress: manager-delegated-intake-absorption-closure-governance

- issue_id: `I-20260326-0445`
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260326-feature-intake-absorption-closure-governance`
- branch: `feature/intake-absorption-closure-governance-20260326`

## What Changed

1. 在 `docs/system/workspace/scripts/runtime/freely` 新增 manager-side absorbed reconciler。
2. 只有当 delegated continuation 本轮进入当前 prompt，且本轮成功产出新的 manager continuity 文件时，才把对应 intake `meta.env` 收为 `STATUS="absorbed"`。
3. absorbed 回写会把 `LINKED_ARTIFACT` 指向真实 continuity 文件，并把 `ABSORPTION_TARGET` 收成 `continuity://manager-supervision`。
4. 保持现有 active-prompt consumed / stop-after-failure returns-to-pending 语义不变。

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-intake-absorption-closure`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `./bin/governance-check`

## Current Judgment

- same-family fix 已进入 canonical `develop`，且 focused verification 在本轮 closeout replay 继续通过。
- 当前将本 issue 收口为 `completed`。
- 该 completed 仅代表 manager-owned delegated intake absorbed closure 达标，不代表相关 owner / worker-side lifecycle 全部完成。
