# Tasks: 补齐 seed 声明并建立 allowlist/seed 一致性检查
- issue_id: I-20261105T062506Z-A
- pre_tests_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062506Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `test-worktree-seed-package-parity`（static + behavior），在未修改真源上跑确认 RED；修正 symlink 源夹具、seeder 路径、macOS /tmp 归一化、shell 变量展开四类夹具问题。
- [x] T2: 实现前评审：逐行核对 allowlist 与 .gitignore，确认仅 1 条 gitignored 条目；核查 seeder 的 required 语义、输出守卫顺序、#4201/#4151 覆盖范围，确认不夹带。
- [x] T3: `worktree-seed.toml` 新增 bootstrap 的 copy / required=false 声明。
- [x] T4: 新增只读 `package-seed-parity.py`，复用 seeder 的 `load()` 真源。
- [x] T5: `bin/freely-package` 在 rm -rf 前置调用检查，保留输出守卫与顺序。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log；7 个相关回归以未修改 develop HEAD 做基线对比，0 新增失败；当前工位残留用封装 seeder 补齐并复跑输出守卫测试。
- [x] T7: 复用既有 story（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、IDN。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
