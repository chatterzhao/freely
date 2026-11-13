# PRD: test-pre-merge 沙箱的受控回收

- issue_id: I-20261113T074432Z-A
- source_raw: raw-20261113T074432Z
- workflow_kind: fix
- milestone: M-20261113T074432Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story）

## 目标

让「dev 工位已收口、只剩 test-pre-merge 沙箱」的残留可以用封装命令回收，
同时 main/develop 的保护强度一点不降。

## 唯一改动范围

- `docs/system/workspace/scripts/worktree/wt-close` 的保护分支守卫（`_is_protected_branch` 调用处）。
- 新增 AT `docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py`。
- 新增 unit `docs/system/workspace/scripts/tests/unit/t-wt-close-premerge-guard-01.sh`。
- `bin/test-all` 的 CORE / CI_CORE 各 +1。

## 不退化边界

- main/develop 仍一律拒绝；`_is_protected_branch` 枚举不变；
- `--force` reason 前缀、closeout-gate 活跃 agent 检查、平台关单通道不变；
- R33.9 的分支解析 / 计数守卫不变；不改 `--dry-run` 行为。

## 功能需求

- FR-1：test-pre-merge-* + FORCE + DISCARD_UNMERGED → 放行并打印 `retiring disposable test sandbox`。
- FR-2：缺任一 flag → 拒绝并提示需要两个 flag 与合规 reason。
- FR-3：main / develop 即使两 flag 齐备仍拒绝。
- FR-4：develop 基线同条件必须拒绝（负向控制）。

## 验收

AT-001 RED `8 ok / 5 failed`（develop `b0686c6fa` 快照 + 基线控制 R1）→ GREEN `12 ok / 0 failed`；
unit `5 ok / 0 failed`；`bin/test-all --ci` 全绿；合并后真机回收残留工位，`git worktree list` 只剩主工位。
