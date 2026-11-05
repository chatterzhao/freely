---
issue_id: I-20261104T083043Z-A
issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/issues/I-20261104T083043Z-A.md
phase_state: completed
---

- issue_id: I-20261104T083043Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/issues/I-20261104T083043Z-A.md

## Implementation Decision Note

- decision: 在 `docs/system/workspace/scripts/worktree/wt-create` 中引入四态幂等状态机与 `_init_test_worktree_state()` 唯一初始化真源；标准模式中断后重跑可只补建 test 工位，legacy 传入 `test-pre-merge-*` 分支名时以对应 dev 分支为 base 执行同一初始化。
- why_this: 根因是部分成功被当作重复创建一律拒绝，且 test 工位初始化内联不可复用。让「正常创建 / 中断恢复 / legacy 补建」三条路径汇聚到同一函数，可避免恢复出的 test 工位缺 seed、`.freely` 状态或 `test-gate.env`，而这三项正是 PR 门禁 `pretests_not_tested` 的判定依据。
- alternatives_considered: ①仅要求调用方加长超时并手工补建——无法覆盖网络/取消，且手工建出的工位缺初始化；②新增 `wt-create --resume` 子命令——自动化轮次只重跑原命令，仍会撞上 Branch already exists，且多一个入口需同步维护；③加 trap 回滚——只能减少新增残留，无法恢复既有残留，列为残余风险而非本 PR 方案。
- boundary_non_goals: 不改 `platform-adapter.py` 的 raw key 漂移；不加事务回滚；不改 `bin/wt-create` shim；不改 `wt-close`；不调整平台同步与超时策略。
- residual_risk: Step 2 中途失败仍可能留下「test 分支已建但初始化未完成」的工位，当前四态判定会把它视为幂等 no-op，不会重跑初始化。后续应增加初始化完成标记并在恢复时校验；本 PR 未覆盖。
