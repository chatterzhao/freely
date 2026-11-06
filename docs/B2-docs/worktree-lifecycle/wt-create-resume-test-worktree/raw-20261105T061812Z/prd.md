# PRD: 四态判定校验工位目录与初始化标记

- issue_id: I-20261105T061812Z-A
- source_raw: raw-20261105T061812Z
- workflow_kind: fix
- milestone: M-20261105T061812Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

让 `wt-create` 的幂等判定以「可用工位」而非「分支存在」为依据，中断残留能自动补齐。

## 唯一改动范围

1. `wt-create` 新增 `_wt_registered_dir()` 与 `_wt_test_initialized()` 两个判定 helper。
2. pre-flight 的 no-op 条件升级为「两分支 + 两注册目录 + test-gate.env 标记」。
3. 恢复路径按缺失项分别补建 dev/test 目录或重跑初始化。
4. 新增行为回归测试 `test-wt-create-four-state-dir`。

## 不退化边界

- `freely_wt_resolve_target_path()` / `worktree-common.sh` 不改（R4/#4191 独立）。
- `_init_test_worktree_state()` 仍是初始化单一真源，三条路径共用。
- 「dev 缺 / test 在」继续拒绝；双工位齐全继续幂等 no-op；legacy 补建与 Q1/#4186 恢复能力不变。
- 顶层 `return 1` 三处不动（本轮自举发现的 #4201 独立 issue）。

## 功能需求

- FR-1: `_wt_registered_dir()` 用 `git worktree list --porcelain` 取实际注册目录并要求目录存在。
- FR-2: `_wt_test_initialized()` 以 `test-gate.env` 含 `^TEST_STATUS=` 为完成标记，接受任意状态值。
- FR-3: 补建已存在分支的工位时不带 `-b`；分支不存在时复用 `_create_worktree`。
- FR-4: 行为测试覆盖 CASE A/B/C/D 四种残留态。

## 验收

见 `verification/pre-tests.md` 与 AT-001 RED/GREEN 证据：13 项检查全 GREEN，4 个既有 wt-create 回归基线对比 0 新增失败。
