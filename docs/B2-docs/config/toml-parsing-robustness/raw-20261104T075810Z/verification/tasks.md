# Tasks: config schema + doctor 可观测类型校验
- issue_id: I-20261104T075810Z-A
- pre_tests_path: docs/B2-docs/config/toml-parsing-robustness/raw-20261104T075810Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真源普查——58 flat key、模板 52 键、gate 静默分支位置、doctor 现有检查项、打包白名单范围。
- [x] T2: 写 AT-001（12 静态/对照 + 8 行为），develop 基线确认 RED `2 ok / 18 failed`。
- [x] T3: 生成 `contracts/config/schema.yaml`（双解析器验证）+ `quality/config_schema.py`（rc 0/1/2）。
- [x] T4: `cmd_doctor` 接线一次；`package-allowlist.txt` 补 `contracts/`。
- [x] T5: GREEN `20 ok / 0 failed`；现场修正主仓/工位 gitignored 配置；回归与不退化核对。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
