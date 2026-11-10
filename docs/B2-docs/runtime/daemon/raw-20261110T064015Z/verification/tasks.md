# Tasks: 派发 CAS 幂等 + SSE watchdog 单实例所有权
- issue_id: I-20261110T064015Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T064015Z/verification/pre-tests.md

## 任务分解

- [x] T1: 工位已由 `wt-create` 建好（只有物化 B1），先 `git merge develop` 同步到 `6715a67a2`（P0 #4272）。重做真源普查：更正「`--expected-status` 被拒」为「`parse_known_args()` 静默吞掉」；否掉「python watchdog 是重复 state_update 消费者」；确认三层启动路径、watch-in-watch 死代码、三处裸 pid 写。证伪 #4155 / #4239 / #4246 / #4272 / #4157 均未覆盖。
- [x] T2: 写最终版 AT-001（11 静态 + 4 DB + 3 CLI + 2 pid）；用 `git archive develop` 隔离基线、只注入 AT-001 跑 RED `2 ok / 18 failed`（2 项 PASS 是守卫）。期间修过一次 AT 自身的 `sys.path`，使基线能真实 import daemon 模块，RED 证据重跑后落盘。
- [x] T3: 四层 CAS：`freely_db_manager.py` 的 `a2a_task.update` 支持 `expected_state` 单条条件 UPDATE；`a2a_server.py` 的 `update_fields` 返回 affected、PATCH 对冲突返回 409 `state_conflict`；`a2a_task.py` 登记 `--expected-state` / `--expected-status`、透传并对冲突 `sys.exit(3)`；`runtime/freely` 派发循环在 launch 之前抢占 `submitted → working`、删除启动后的 A2A 状态写。
- [x] T4: SSE 所有权：`runtime/freely` 新增 `sse_watchdog_claim_pid`（fcntl.flock + 存活 pid + 可选 cmdline owner 校验，owner 不可验证时 fail-closed）；`sse-watchdog.sh` 与 `_start_watchdog_sse_py` 改走 claim helper（重复 python 实例被 reaped）；`cmd_ensure_sse_watchdog_watch` 改为监督循环，只经 `launch_sse_watchdog` 启动，不再写自身 `$$`、不再嵌套 consumer。
- [x] T5: GREEN `20 ok / 0 failed`（首轮 `18 ok / 2 failed` 抓到 DB handler 参数顺序 bug，修正后全绿）；新 AT 同时接入 `bin/test-all` 的 `CORE` / `CI_CORE`；11 项回归 + 两个状态文件 lint 全绿；`bin/test-all --ci` `7 ok / 0 failed`；local 唯一失败为既有 known-broken。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity / 真源普查） |
| T3, T4 | AT-001（静态 11 项） |
| T3 | AT-001（DB 行为 4 项 + CLI 行为 3 项） |
| T4 | AT-001（并发 pid 2 项） |
| T5 | AT-001 GREEN + 回归 + CI 接线 |
