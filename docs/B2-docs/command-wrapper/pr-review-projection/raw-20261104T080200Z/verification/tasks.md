# Tasks: pr-review-guarded 迁回 scripts/
- issue_id: I-20261104T080200Z-A
- pre_tests_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261104T080200Z` 建工位；盘点 `bin/` 99 个入口，38 个超 40 行。
- [x] T2: 判定「超阈值 ≠ 该迁移」；收敛为「迁移 pr-review-guarded + 注册表 + 门禁 + 清单 + 后续 raw」。
- [x] T3: 实现移到 `scripts/worktree/pr-review-guarded`（改 `ROOT_DIR` 推导），`bin/` 变 4 行投影。
- [x] T4: 生成 `bin-projections.yaml`（38 条，dispatcher 3 / impl 35，impl 挂 `raw-20261111T125724Z`）。
- [x] T5: 新增 `bin/check-bin-projection`（0/1/2，三条拒绝路径）与 `bin-inventory.md`（99 行清单）。
- [x] T6: AT-001 进 `CORE`/`CI_CORE`；`epic-command-wrapper` 注册 `pr-review-projection` story。
- [x] T7: 用 `freely feedback` 建 `raw-20261111T125724Z` / #4302 承接剩余 35 条 impl。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1–T3 | AT-001（静态 1–3、行为 16） |
| T4–T5 | AT-001（静态 4–10、行为 13–15） |
| T6 | AT-001（静态 11–12） |
| T7 | 范围标注（另立 raw） |
