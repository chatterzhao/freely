# Tasks: wt-create 顶层 return 改为 exit
- issue_id: I-20261106T084804Z-A
- pre_tests_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261106T084804Z/verification/pre-tests.md

## 任务分解

- [x] T1: 实现前评审：括号深度分析定位顶层 3 处 return、核对函数内 22 处合法 return、确认 shim 是 `exec bash`、逐条证伪 #4153/#4157。
- [x] T2: 编写 `test-wt-create-top-level-return`（static + behavior），在未修改真源上跑确认 RED；修正夹具（stub 必须真实物化 issue.md，否则三条分支都在 pull 阶段提前失败）。
- [x] T3: 三处顶层 `return 1` 改为 `exit 1`，不触碰其他任何行。
- [x] T4: 跑 GREEN；以未修改 develop HEAD 做基线 RED 与 10 个相关回归对比，0 新增失败。
- [x] T5: 复用既有 story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T6: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3 | AT-001 |
| T4, T5, T6 | AT-001 |
