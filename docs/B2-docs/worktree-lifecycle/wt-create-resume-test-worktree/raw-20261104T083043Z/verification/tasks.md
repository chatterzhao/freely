# Tasks: wt-create 中断恢复与 test-pre-merge 工位补建
- issue_id: I-20261104T083043Z-A
- pre_tests_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写脚本级回归测试 `docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree`（static 断言组 + e2e 隔离仓库组），先跑确认 RED。
- [x] T2: 抽出 `_init_test_worktree_state()`，收纳 seed、`.freely` 状态克隆、`test-gate.env` 初始化；标准模式 Step 2 改为调用它。
- [x] T3: 实现标准模式四态幂等：`resume_mode` 判定、恢复分支、幂等 no-op、不一致拒绝；恢复模式跳过 replica 检查、fuzzy-match 与远程 fetch。
- [x] T4: legacy 模式识别 `test-pre-merge-<key>-<slug>`，定位 dev 分支作为 base 并复用初始化函数；同步修正 usage 帮助文本。
- [x] T5: 执行 GREEN，记录 AT-001/AT-002 的 RED/GREEN 证据日志，更新 pre-tests 状态字段。
- [x] T6: 更新 `docs/epics-map.svg` 的 worktree-lifecycle story 节点并运行 `freely check-epics-map`。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T4 | AT-001 |
| T1, T2, T3 | AT-002 |
