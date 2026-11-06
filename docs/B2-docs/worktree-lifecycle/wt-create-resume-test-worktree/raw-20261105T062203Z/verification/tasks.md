# Tasks: 恢复模式按 git 登记反查 dev 工位真实路径
- issue_id: I-20261105T062203Z-A
- pre_tests_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062203Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `test-wt-create-recovery-dev-path`（static + behavior），在未修改真源上跑确认 RED 并记录证据；修正 macOS /tmp 符号链接与 static 提取范围两类夹具问题。
- [x] T2: 实现前评审：逐处核对 `freely_wt_resolve_target_path` 的 4 个调用点，区分「新建避让」（保留）与「已有工位反查」（修复）；确认 R3 的 `_wt_registered_dir()` 可复用、#4201 边界不夹带。
- [x] T3: 恢复块写 scan state 前用 `_wt_registered_dir "$dev_branch"` 反查；失败或与 `_dev_dir` 不一致均报错退出。
- [x] T4: `_update_scan_state` 与恢复摘要 `dev (kept):` 均改用反查结果。
- [x] T5: 跑 GREEN，写 AT-001-GREEN.log；7 个相关回归测试零新增失败。
- [x] T6: 复用既有 story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
| T5, T6 | AT-001 |
