# Tasks: cooldown 族迁移到安全协议
- issue_id: I-20261110T074344Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T074344Z/verification/pre-tests.md

## 任务分解

- [x] T1: 选定 cooldown 族（1 读/1 写/2 键），核对下游只用 `CROSS_TOOL_SWITCH_*`。
- [x] T2: 写 AT-001（2 静态 + 6 行为，source 真实 freely），基线确认 RED `2 ok / 6 failed`。
- [x] T3: `state_file.py` 加 `values` 与 `write --kv`，兼容既有 `read`/`--data`/`to-shell`。
- [x] T4: 改写 `_read/_write_cooldown_state`（bash 3.2 用 `read` 而非 `mapfile`）；GREEN `8 ok / 0 failed`、source 55→54、回归全绿。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
