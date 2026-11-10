# Tasks: 平台写收口到 adapter
- issue_id: I-20261104T080014Z-A
- pre_tests_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261104T080014Z/verification/pre-tests.md

## 任务分解

- [x] T1: 建 feature/test 工位（基于 `9348b2661`）。普查 4 种直连写与 adapter 现有 `create-issue`/`update-issue`/`close-multi`（0/3/1 已实现）；确认拆文件与 `feedback` 逐字对齐不在本轮。
- [x] T2: 写 AT-001（3 静态 + 1 行为），基线 RED `0/4`。
- [x] T3: adapter 新增 `issue-write-one`（create/comment/close/update 路由到 handler）；`_repo()` 支持 `FREELY_PLATFORM_REPO`。
- [x] T4: issue-sync 4 个 `_gh_*` 改调 adapter；url 提取止于引号；`GH_REPO` 经 env 传入。
- [x] T5: GREEN `4/0`；补 promote-b2 夹具 adapter 依赖（恢复 23/0）；replica-guard stub 增加 `issue-write-one`；`test-all --ci` 10/0。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3, T4 | AT-001（静态 3 + 行为 1） |
| T5 | 回归 + CI |
