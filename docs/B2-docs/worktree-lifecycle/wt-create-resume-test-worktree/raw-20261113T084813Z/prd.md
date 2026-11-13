# PRD: 恢复 protected 门禁与 companion-only 沙箱回收

- issue_id: I-20261113T084813Z-A
- source_raw: raw-20261113T084813Z
- workflow_kind: fix
- milestone: M-20261113T084813Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story）

## 目标

把 R33.9/R33.10 为回收一个残留沙箱而放宽的 protected 门禁恢复原强度，
并通过**修实现**（Phase 6b 覆盖不足）来补齐残留沙箱回收能力。

## 唯一改动范围

- `docs/system/workspace/scripts/worktree/wt-close`：guard、resolver、新增 companion-only 函数与解析标记。
- 更新既有 2 个 AT + 2 个 unit（它们是 R33.9/R33.10 的产物，随实现同步修正）。
- `projection.lock` 重录 1 条（`bin/wt-close` delegate 投影 hash 变化）。

## 不退化边界

- main/develop/test-pre-merge 主路径一律 protected；`_is_protected_branch` 枚举不变；
- `--force` reason 前缀、closeout-gate、ambiguous 拒绝、R33.7 dry-run、R33.9 `_count` 守卫不变；
- 不改平台 adapter、不删 Phase 7 代码；不手工删 worktree/分支。

## 功能需求

- FR-1：守卫对三类 protected 分支无条件拒绝。
- FR-2：resolver 不解析 test-pre-merge-*；无 fix/feature 分支时交给 companion-only 路径。
- FR-3：companion-only 要求 `--force` + `--discard-unmerged`（reason gate 已校验前缀），唯一沙箱，只删工位+分支。
- FR-4：companion-only 不产生平台关单 / Phase 7 develop 同步；`--dry-run` 零副作用。
- FR-5：develop 基线复现被放宽的守卫与 resolver 回退（负向控制）。

## 验收

两个 AT 均 RED→GREEN（guard `8 ok / 12 failed` → `18 ok / 0 failed`；count `10 ok / 2 failed` → `11 ok / 0 failed`），
两个 unit `6 ok / 0 failed` 与 `7 ok / 0 failed`；`bin/test-all --ci` 全绿；三门禁不变。
