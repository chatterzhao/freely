# Tasks: 接线 commit-msg 提交期阻断
- issue_id: I-20261103T132509Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261103T132509Z/verification/pre-tests.md

## 任务分解

- [x] T1: 实现前评审：精读孤儿真源与 pr-merge-guarded trailer/handshake 生命周期；验证真实历史 25 条 commit 通用规范兼容性；识别 test 工位自锁风险；证伪现有 open issue 覆盖。
- [x] T2: 探针实证 `git merge --continue` 触发 commit-msg hook 且受控状态可见；写 AT-001 RED（隔离仓库真实 merge）；修正夹具 ENOENT 噪音与静态断言误匹配。
- [x] T3: 新增 `.githooks/commit-msg` shim（复用 R8 fail-closed 模板）。
- [x] T4: `commit-msg.sh` 增加受控 handshake 校验、收窄 receipt 分支到 develop/main、修复 pipefail 静默退出与 stderr 路由。
- [x] T5: `hooks/README.md` 补三层治理的 commit-msg 已接线说明。
- [x] T6: 跑 GREEN 与 13 个回归基线对比，0 新增失败；自举发现 #4211 用 freely feedback 立项并排入 goal R9.5。
- [x] T7: 复用 `gate/governance` story，`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T8: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7, T8 | AT-001 |
