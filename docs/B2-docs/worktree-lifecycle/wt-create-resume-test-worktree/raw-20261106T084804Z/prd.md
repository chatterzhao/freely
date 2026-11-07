# PRD: wt-create 顶层 return 改为 exit

- issue_id: I-20261106T084804Z-A
- source_raw: raw-20261106T084804Z
- workflow_kind: fix
- milestone: M-20261106T084804Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

让 `wt-create` 三条失败分支输出业务错误而非 bash 语法错误，失败语义由显式 `exit 1` 表达，不依赖 `set -e` 隐式兜底。

## 唯一改动范围

`wt-create` 主流程顶层三处 `return 1`（998 / 1018 / 1026）改为 `exit 1`。新增回归测试 `test-wt-create-top-level-return`。

## 不退化边界

- 函数内 22 处 `return` 不改；`bin/wt-create` 的 `exec bash` shim 不改。
- 三条业务错误文案、所有清理动作（`git worktree remove --force` / `git branch -D` 带 `|| true`）逐字不变。
- 四态幂等判定、恢复模式、legacy 补建、`_init_test_worktree_state()` 单一真源不动。
- #4153（方向相反）、#4157（不同文件）不夹带；2 个预存红测试归 #4151。

## 功能需求

- FR-1: 三处失败分支 exit 1、输出含业务错误文案、不含 `can only return` 语法错误。
- FR-2: 失败后 dev 分支清理，不产生半成品工位。
- FR-3: 顶层 return 计数 0、函数内 return 数保持 22、`bash -n` 通过。
- FR-4: 回归测试覆盖三条分支与基线退化审计。

## 验收

AT-001 基线 RED 4 项失败 / 12 项既有能力 PASS → GREEN 20 项全通过；9 个回归 PASS + 2 个预存红测试与基线一致 → 0 新增失败。
