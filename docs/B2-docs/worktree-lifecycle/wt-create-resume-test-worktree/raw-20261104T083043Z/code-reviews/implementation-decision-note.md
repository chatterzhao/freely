---
issue_id: I-20261104T083043Z-A
issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/issues/I-20261104T083043Z-A.md
phase_state: completed
---

- issue_id: I-20261104T083043Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/issues/I-20261104T083043Z-A.md

## Implementation Decision Note

- decision: 在 `docs/system/workspace/scripts/worktree/wt-create` 中引入四态幂等状态机与 `_init_test_worktree_state()` 唯一初始化真源；标准模式中断后重跑可只补建 test 工位，legacy 传入 `test-pre-merge-*` 分支名时以对应 dev 分支为 base 执行同一初始化；同时修复接口判定，改为按调用方实际传入的参数区分标准/legacy 模式，使 legacy 分支真正可达。
- why_this: 根因是部分成功被当作重复创建一律拒绝、test 工位初始化内联不可复用，以及接口判定把默认非空的 `skill_path` 计入 `using_new` 导致 legacy 分支恒不可达。前两者让「正常创建 / 中断恢复 / legacy 补建」三条路径汇聚到同一函数，避免恢复出的 test 工位缺 seed、`.freely` 状态或 `test-gate.env`（PR 门禁 `pretests_not_tested` 的判定依据）；第三者若不修，补建代码就是 dead code，帮助文本会承诺一个根本无法触发的能力。PR review 阶段在隔离仓库实测确认该缺陷后，以 AT-003 行为测试补上回归守护。
- alternatives_considered: ①仅要求调用方加长超时并手工补建——无法覆盖网络/取消，且手工建出的工位缺初始化；②新增 `wt-create --resume` 子命令——自动化轮次只重跑原命令，仍会撞上 Branch already exists，且多一个入口需同步维护；③加 trap 回滚——只能减少新增残留，无法恢复既有残留，列为残余风险而非本 PR 方案。
- boundary_non_goals: 不改 `platform-adapter.py` 的 raw key 漂移；不加事务回滚；不改 `bin/wt-create` shim；不改 `wt-close`；不调整平台同步与超时策略。
- residual_risk: ①Step 2 中途失败仍可能留下「test 分支已建但初始化未完成」的工位，当前四态判定会把它视为幂等 no-op，不会重跑初始化；②四态判定只检查分支是否存在，不检查 worktree 目录是否仍在——分支保留而工位目录被移除时，no-op 会误判为「已存在」，恢复模式也不会补回 dev 工位目录。两者都应增加「初始化完成标记 + 工位目录存在性」校验；本 PR 未覆盖，属已记录的后续治理项。
