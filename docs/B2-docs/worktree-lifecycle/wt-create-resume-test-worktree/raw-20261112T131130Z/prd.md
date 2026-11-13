# PRD: wt-close 分支解析数值守卫与残留工位回收

- issue_id: I-20261112T131130Z-A
- source_raw: raw-20261112T131130Z
- workflow_kind: fix
- milestone: M-20261112T131130Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

1. `wt-close --raw-key <key>` 在无匹配分支时不再抛 `[[ 0\n0 -eq 0 ]]` 语法错误，也不再静默成功；
2. 只有 `test-pre-merge-<key>-*` 沙箱的残留工位可以用封装命令真正回收。

## 唯一改动范围

- `docs/system/workspace/scripts/worktree/wt-close` 的 `_resolve_branch_from_raw_key`：计数守卫 + 数值校验 + test-pre-merge 单匹配回退。
- 新增 AT `docs/system/workspace/scripts/tests/test-wt-close-branch-count.py`。
- 新增 unit `docs/system/workspace/scripts/tests/unit/t-wt-close-count-01.sh`。
- `bin/test-all` 的 CORE / CI_CORE 各 +1。

## 不退化边界

- closeout-gate / pretests-retirement-gate / dev-test 一致性判据不变；
- `--force` / `--discard-unmerged` 语义、reason 前缀要求不变；
- ambiguous 分支仍拒绝；平台关单仍只经封装命令；
- 正常 fix/feature 分支解析结果逐字不变。

## 功能需求

- FR-1：`grep -c` 无匹配时只得到一个 `0`，`[[ ... -eq 0 ]]` 不再抛语法错误。
- FR-2：`_count` 必须是单个数字，否则打印诊断并 `return 1`。
- FR-3：无 fix/feature/hotfix 分支时，唯一的 `test-pre-merge-<key>-*` 分支可被解析。
- FR-4：两个等长候选仍 `DENIED ambiguous` 且非零退出。
- FR-5：develop 基线同一行为断言必须复现语法错误（RED 真实）。

## 验收

AT-001 RED `5 ok / 7 failed`（develop `1a6139375` 快照 + 基线控制 R1 pass）→ GREEN `11 ok / 0 failed`；
unit `5 ok / 0 failed`；`bin/test-all --ci` 全绿；合并后真机回收自证残留工位。
