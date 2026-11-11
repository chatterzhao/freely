# Tasks: runtime 拆分第一阶段
- issue_id: I-20261104T075849Z-A
- pre_tests_path: docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261104T075849Z --source platform --kind feature` 建 dev/test 工位；普查确认单体 27,272 行 / 944 函数 / 56 个 `cmd_*`、`check-file-size` 为 skip。
- [x] T2: 脚本解析 944 个顶层函数，生成依赖矩阵并分 phase（0=15、1=6、2=22、3=13），据此选定 3 个外移目标。
- [x] T3: 写 AT-001（12 静态 + 4 行为）；develop `d33855eb0` 基线 RED `0 ok / 16 failed`。
- [x] T4: 新增 `runtime/lib/common.sh`（7 个 helper），单体改为守卫式 source 并删除内联定义。
- [x] T5: 外移 `bin/test-gate`（run/record + 2 个私有 helper）与 `bin/evidence`（add）；单体三处变 `exec` 投影。
- [x] T6: 新增 `bin/check-runtime-size` + `runtime/.size-budget`（27,158）；新增 `split-plan.md` 与 `rust-migration-poc.md`。
- [x] T7: 新增 `tests/unit/t-runtime-split-01.sh`（24 断言）；AT 进 `CORE`/`CI_CORE`；`epic-runtime` 注册 `runtime-split` story。
- [x] T8: 吃狗粮回归：修 R30 AT 的「数组第一行」脆弱断言，两个 AT 共用 `array_has()`；GREEN 16/0、unit 98/0、CI 19/0、epics 17/214。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T3 | AT-001（RED fidelity） |
| T4 | AT-001（静态 2–4） |
| T5 | AT-001（静态 1、5–6 + 行为 14–16） |
| T6 | AT-001（静态 7–9、12 + 行为 13） |
| T7 | AT-001（静态 10–11）+ unit |
| T8 | 回归/CI 与附带修复 |
