# Tasks: supervisor 失败退出码 + Python 版本前置
- issue_id: I-20261103T132644Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261103T132644Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create` 建 fix/test 工位（基于 `502496df1`）。前置评审 8 个分项：分项 5 的 output 守卫已由 #4158 落地（`refuse_dangerous_output` 已存在）、不走；本轮只做分项 1 + 6a，其余 6 项由一条汇总 raw 承接。
- [x] T2: 写最终版 AT-001（3 静态 + 3 行为）；`git archive develop` 基线 RED `2 ok / 4 failed`（守卫为 stub 新版本与真实环境）。首版 stub 的 realpath 参数位置写错（`$2` → `$3`），修正后 RED 才可信。
- [x] T3: `runtime/freely` 的 `will now stop` 分支 `exit 0` → `exit 1`，事件补 `exit_kind=degraded_no_recovery`；`bin/freely` 在 `_SCRIPT` 之前加 `command -v python3` 与 `sys.version_info >= (3, 11)` 检查，失败文案含 `Python >= 3.11`。
- [x] T4: GREEN `6 ok / 0 failed`；新 AT 接入 `bin/test-all` 的 `CORE`/`CI_CORE`；11 项回归（CLI help / 并发 / DB / 派发 / 契约 / wt-create / materialize）+ `test-all --ci` `9 ok / 0 failed`；local 仅既有 known-broken。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity / 前置评审） |
| T3 | AT-001（静态 3 + 行为 3） |
| T4 | AT-001 GREEN + 回归 + CI 接线 |
