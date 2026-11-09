# Tasks: 测试证据链可验证并替换 CI 桩
- issue_id: I-20261103T132548Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261103T132548Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真机隔离夹具复现手写三行 env 让门禁返回 0；核对 CI 桩与 gate 读侧；证伪 #4216/#4146/#4147/#4198/#4075。
- [x] T2: 写 AT-001（12 静态 + 8 行为），基线快照确认 RED `4 ok / 21 failed`。
- [x] T3: 新增 `test-evidence.py` 单一真源（write/validate/manifest-add）。
- [x] T4: runtime 新增 `test-gate run` / `evidence add` 并接 dispatcher/usage。
- [x] T5: `pretests-retirement-gate` 接入证据校验（fail-closed）。
- [x] T6: `bin/test-all` 聚合入口 + 两个真实 CI 文件。
- [x] T7: GREEN `25 ok / 0 failed` + 17 个回归基线对比。
- [x] T8: B1/B2/milestone/review 落盘；用 `test-gate run` 真机写证据后按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5, T6 | AT-001 |
| T7, T8 | AT-001 |
