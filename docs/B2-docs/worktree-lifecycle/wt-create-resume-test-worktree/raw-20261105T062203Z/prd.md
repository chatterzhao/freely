# PRD: 恢复模式按 git 登记反查 dev 工位真实路径

- issue_id: I-20261105T062203Z-A
- source_raw: raw-20261105T062203Z
- workflow_kind: fix
- milestone: M-20261105T062203Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

恢复摘要与 `scan_state_worktree` 指向真实存在的 dev 工位，避免自动化或人按错误路径进入工位失败。

## 唯一改动范围

恢复块的 2 处 `freely_wt_resolve_target_path "$dev_branch"` → `_wt_registered_dir "$dev_branch"` 反查结果；新增反查失败与一致性校验；新增行为回归测试。

## 不退化边界

正常创建 / test 工位新建 / legacy 补建的 `freely_wt_resolve_target_path` 调用原样保留（它们确实是新建，需要冲突避让）；`_init_test_worktree_state()` 单一真源不变；R3 四态判定、no-op、不一致拒绝不变；顶层 `return 1` 三处不动（#4201 独立）；`worktree-common.sh` 不改。

## 功能需求

- FR-1: 恢复路径在写 scan state 前反查 dev 工位真实路径。
- FR-2: 反查失败或与 pre-flight `_dev_dir` 不一致时明确报错退出，不猜路径。
- FR-3: 恢复摘要与 `_update_scan_state` 均使用反查结果。
- FR-4: 行为测试覆盖摘要/scan state/test 初始化/幂等。

## 验收

见 `verification/pre-tests.md` 与 AT-001 RED/GREEN 证据：8 项检查全 GREEN，7 个相关回归零新增失败。
