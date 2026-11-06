# Tasks: 四态判定校验工位目录与初始化标记
- issue_id: I-20261105T061812Z-A
- pre_tests_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T061812Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `test-wt-create-four-state-dir`（static + behavior 四态），在未修改真源上跑确认 RED 并记录证据。
- [x] T2: 实现前评审：核对 `freely_wt_resolve_target_path` 的「新建目标」语义、R4/#4191 边界、_init_test_worktree_state 单一真源，确认不夹带。
- [x] T3: 新增 `_wt_registered_dir()` 与 `_wt_test_initialized()` 两个判定 helper。
- [x] T4: pre-flight no-op 升级为「两分支 + 两注册目录 + 初始化标记」五项判定，并输出具体缺失项。
- [x] T5: 恢复路径按残留项分别补建 dev/test 目录（已存在分支不带 -b）或重跑初始化。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log；4 个既有 wt-create 回归以未修改 develop HEAD 做基线对比，0 新增失败。
- [x] T7: 自举评审发现顶层 `return 1` 缺陷，证伪 #4153/#4157 覆盖后用 `freely feedback` 创建 #4201 并排入 goal R6.5；本 PR 不夹带修复。
- [x] T8: 复用既有 story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7, T8 | AT-001 |
