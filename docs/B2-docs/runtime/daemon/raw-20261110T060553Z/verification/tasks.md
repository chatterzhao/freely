# Tasks: 状态文件安全协议（第一阶段）
- issue_id: I-20261110T060553Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T060553Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核 issue 证据——55 处状态 source（原报 20）、39 处非状态 source、77 键、位置格式文件、`load_meta_env_snapshot` 先例。
- [x] T2: 写 AT-001（2 静态 + 7 行为，含可执行 PoC），基线确认 RED `1 ok / 7 failed`。
- [x] T3: 实现 `runtime/state_file.py`（新格式 + 兼容旧格式不展开 + 白名单 + to-shell）。
- [x] T4: 实现 `bin/check-state-file-sources`（55 基线只降不升、禁止 eval/exec）；GREEN `9 ok / 0 failed` + 回归全绿。
- [x] T5: 拆出 `raw-20261110T074344Z`（55 读/15 写逐组迁移）并排进 goal。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
