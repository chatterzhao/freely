# B1 Candidates — raw-20261113T084813Z

## C-20261113T084813Z-A：恢复 protected 门禁 + companion-only 回收

- kind: fix
- 范围（`docs/system/workspace/scripts/worktree/wt-close`）：
  1. 恢复 `_is_protected_branch` 守卫对 `test-pre-merge-*` 的一律拒绝，删除 R33.10 的 `--force --discard-unmerged` 例外。
  2. 撤销 `_resolve_branch_from_raw_key` 的 test-pre-merge 回退（保留 `_count` 数值守卫：真 bug 修复，不动）。
  3. 新增 `_wt_retire_orphan_test_sandbox`：解析阶段无 fix/feature 分支时设置 `ORPHAN_SANDBOX_KEY`，在 `_require_reason` 之后走专门回收——要求 `--force` + `--discard-unmerged`、唯一同 key 沙箱、`git worktree remove` + `git branch -D`；支持 `--dry-run` 零副作用；**不**触发平台关单 / Phase 7 develop 同步。
  4. 更新 `test-wt-close-test-premerge-guard.py`（静态 8 + 行为 8 + 基线控制 2）、`test-wt-close-branch-count.py`（静态 6 + 行为 5 + 基线控制 1）与两个 unit。
- 验收：
  - test-pre-merge / develop / main 即使两 flag 齐备仍被守卫拒绝；fix 分支不受影响；
  - sandbox git 仓库里 companion-only 真的删掉分支与工位（**在临时目录存活期内查询，避免假绿**），且不产生平台/develop 副作用；缺 `--force` 拒绝；dry-run 零副作用；
  - resolver 不再把沙箱解析成 close target；`_count` 数值守卫保留；
  - develop 基线必须复现「守卫有 --force 例外」与「resolver 解析沙箱」两项红。
- 不退化边界：
  - main/develop 保护、reason 前缀校验、closeout-gate 活跃 agent 检查、ambiguous 拒绝不变；
  - R33.7 的 `--dry-run` 零副作用、R33.9 的 `_count` 数值守卫不变；
  - 不删 Phase 7 逻辑，但不得由沙箱回收触发；不手工删 worktree/分支。
