# Tasks: 门禁 fail-open 收敛为 fail-closed
- issue_id: I-20261103T132458Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261103T132458Z/verification/pre-tests.md

## 任务分解

- [x] T1: 实现前评审：逐个 shim 核对真身存在性与触发场景，识别 `post-checkout` 独立性、外部项目合法早退、file-size 历史 errors 自锁风险、正常无 raw key 路径；确认 AGENTS.md 约束方向。
- [x] T2: 编写 `test-gate-fail-closed`（static + 3 个隔离 git 仓库行为用例），在未修改 develop 真源上跑确认 RED；修正静态断言模式、CASE C 阈值、sentinel 路径、每个 shim 都需真身、多一个 `fi` 等夹具问题。
- [x] T3: 6 个 shim 改 `-f` + `exit 2`；`post-checkout` 不动。
- [x] T4: `pre-commit.sh` hooksPath / helper / 门禁真身守卫全部 fail-closed，并区分自举与外部项目。
- [x] T5: `pr-create-guarded` 4 处 skipping 改 `[ERROR]` + exit 2；`checkpoint-guard` 默认严格。
- [x] T6: `check-file-size` 新增 `--staged-only` 增量模式 + 全量扫描覆盖无扩展名脚本，接入 pre-commit。
- [x] T7: 真实工位 `git commit` 冒烟验证不自锁；跑 GREEN 与 14 个回归基线对比，0 新增失败。
- [x] T8: 复用 `gate/governance` story，`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。
- [x] T9: 按封装命令收口：`issue-sync close` → `pr-create-guarded` → 独立人工 review → `pr-merge-guarded` → `wt-close` → 重新打包部署 → 更新 goal / memory。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5, T6 | AT-001 |
| T7, T8, T9 | AT-001 |
