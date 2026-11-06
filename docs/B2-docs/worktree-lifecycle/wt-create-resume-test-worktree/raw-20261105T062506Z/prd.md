# PRD: 补齐 seed 声明并建立 allowlist/seed 一致性检查

- issue_id: I-20261105T062506Z-A
- source_raw: raw-20261105T062506Z
- workflow_kind: fix
- milestone: M-20261105T062506Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

由 `wt-create` 新建的工位无需人工复制即可跑通打包与打包相关测试；新增位于 gitignored 路径的打包白名单条目若未同步 seed 会被拦下。

## 唯一改动范围

1. `worktree-seed.toml` 新增 `.freely/tool-boundary-bootstrap.md`（copy / required=false）。
2. 新增只读一致性检查 `docs/system/workspace/scripts/quality/package-seed-parity.py`。
3. `bin/freely-package` 在 `rm -rf` 前置调用该检查。
4. 新增回归测试 `test-worktree-seed-package-parity`。

## 不退化边界

- `worktree_seed.py` / `wt-create` / `_init_test_worktree_state()` / allowlist 内容不改。
- 输出路径守卫（#4158）及其在 rm 之前的顺序不变；allowlist 复制循环行为不变。
- 新 seed 条目 required=false（**不新增**硬失败点）；干净 clone 上既有的 `.freely/agent-table.toml required=true` 行为不在本 issue 范围，见 B1 brainstorms §不退化边界。
- 顶层 `return 1`（#4201）、R3 四态、R4 反查、Q2 标题契约均不动。

## 功能需求

- FR-1: seeder 把 bootstrap 复制进新工位，工位拥有自己的副本（非 link）。
- FR-2: checker 只读比对「gitignored allowlist 条目」与「seed manifest 声明」，复用 seeder 的 `load()` 真源，未声明则点名并 exit 1。
- FR-3: 打包在清理输出之前执行该检查，fail-closed。
- FR-4: 回归测试覆盖最小 seed 项目真实打包、未声明条目被拦下、守卫顺序、7 个相关回归零新增失败。

## 验收

见 `verification/pre-tests.md` 与 AT-001 RED/GREEN 证据：13 项检查全 GREEN，7 个相关回归基线对比 0 新增失败。
