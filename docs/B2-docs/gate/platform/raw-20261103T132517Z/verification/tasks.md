# Tasks: SDD frontmatter 解析所有权收口
- issue_id: I-20261103T132517Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261103T132517Z/verification/pre-tests.md

## 任务分解

- [x] T1: 逐行核对三套解析器（契约模块、scan 手写切片、issue-sync 内联 python），实测 12+1 份 B1 坏文档形态，证伪 #4183/#4184/#4216/#4151 的覆盖范围。
- [x] T2: 写 AT-001（9 静态 + 12 行为），develop 基线快照确认 RED `7 ok / 14 failed`。
- [x] T3: `raw_metadata_contract` 增加 `validate_issue_text` / `parse_issue_text` / `validate_issue_path`，`read_issue` 把 YAML 异常包成 `MetadataValidationError`。
- [x] T4: `task-lifecycle-scan.py` 删除手写 `yaml.safe_load` 与 fallback 行解析，改调 `parse_issue_text`；解析失败写 `metadata_validation_error`（B1 与 B2 两条读取路径都覆盖）。
- [x] T5: `bin/issue-sync` 的 `_fm_get` / `_fm_set` / `_fm_has_key` 改为薄封装，走单一所有者 CLI，33 处调用点语义不变。
- [x] T6: 新增 `frontmatter_contract_cli.py`（get / has-key / set / check / repair），repair 默认 dry-run、`--apply` 幂等。
- [x] T7: 修完 23 份存量坏文档（12 B1：11 个 glued `---` + 1 个冲突标记；11 B2：6 个 YAML 内混入 bullet 行 + 5 个相邻字段粘连）。
- [x] T8: **不退化处置**：保留 legacy bullet 格式解析；YAML 有效时不补 bullet（精确复刻收口前语义）；冲突标记改为成对匹配（避免误伤正文 `=======` setext 分隔线）；把 4 个测试夹具补上单所有者 CLI 依赖。
- [x] T9: GREEN `21 ok / 0 failed` + 18 项回归基线对比 + 全量 1082 份文档解析差异定性；B1/B2/milestone/review 落盘后用封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5, T6 | AT-001 |
| T7, T8 | AT-001 |
| T9 | AT-001 + 18 项回归 |
