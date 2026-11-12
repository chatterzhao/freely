# Tasks: 投影一致性检查
- issue_id: I-20261104T080259Z-A
- pre_tests_path: docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261104T080259Z` 建工位；普查 `.githooks/`（6 个非 wrapper 文件）、8 个 wrapper、`post-checkout` 是 105 行实现、生成器 6 处 + 模板 3 处幽灵 skill 名。
- [x] T2: 写 AT-001（16 静态 + 4 行为）；develop `27e91e50c` 基线 RED `1 ok / 19 failed`。
- [x] T3: `git rm` 6 个非 wrapper 文件；`post-checkout` 迁到 `workspace/hooks/post-checkout.sh`（自解析根）+ 11 行 wrapper；三种入参冒烟。
- [x] T4: 修生成器 6 处 + 模板 3 处幽灵 skill 名（改 workflow-guarded / RED-dev-GREEN 三阶段、`--skill` 改 `--kind`）。
- [x] T5: 新增 `quality/projection_verify.py`（record/verify、copy 与 delegate 双语义、agents 名字集合校验、skills machine-local lock）。
- [x] T6: `bin/projections` 投影 + runtime 内联 exec 分派（**被 R31 行数门禁拦下后改用内联先例，预算未上调**）；`deploy-skills` 部署后写回 hash。
- [x] T7: 新增 `tests/unit/t-projection-01.sh`（13 断言）；AT 进 `CORE`/`CI_CORE`；`epic-gate` 注册 story。
- [x] T8: GREEN 20/0；unit 17 文件 111/0；CI 21/0；三个门禁全过；七个既有 AT 全绿。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3 | AT-001（静态 1–4） |
| T4 | AT-001（静态 13–14） |
| T5 | AT-001（静态 5–11 + 行为 17–19） |
| T6 | AT-001（静态 12 + 行为 20）+ unit |
| T7 | AT-001（静态 15–16）+ unit |
| T8 | 回归 / CI / 门禁 |
