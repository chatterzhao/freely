# Pre-Tests: 消除启动锁 TOCTOU 与 DB daemon 双实例
- issue_id: I-20261103T132622Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 并发启动时只允许一个 supervisor 过门（不再因 `state_file_missing` 误回收）、PID 复用不会让活锁白等或让死锁永存；并发 `ensure_freely_db` 只产生一个 daemon、一个 socket，孤儿 daemon 退出不删健康 daemon 的文件
- acceptance_target: 单项目单控制面、单 DB daemon；并发后果从「AI 行为怪异」变成「第二个明确拒绝」
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `freely` 函数（source 后调用）+ 真实 `freely_db_manager.py` 子进程并发 + 隔离临时项目目录与 `/tmp/freely-db-<hash>` 路径；develop HEAD 基线快照对比
- required_evidence: 5 静态 + 4 启动锁行为 + 4 DB 并发行为共 13 项全 GREEN；develop 基线 RED `5 ok / 8 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-concurrency-singletons.py
- test_command: python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
- expected_output: SUMMARY: 13 ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok / 8 failed（静态 5 全缺；TOCTOU 窗口仍回收并抢到锁；DB 并发后 pid 文件指向错误进程、无单实例文案；4 项 PASS 是既有能力守卫——老目录回收、活 owner 阻塞、cmdline 不可读时保守、SQLite 自身锁让第二个恰好崩掉）
- actual_RED_output: develop `c31b73724` 基线快照注入最终版 AT-001 → `SUMMARY: 5 ok, 8 failed`（AT-001-RED.log）。关键证据：`pid file belongs to the surviving daemon ('94129' vs 94128)` —— pid 文件记录的是已死进程，正是 issue 描述的「孤儿覆盖 pid」；且 loser 输出为 `[ERROR] daemon start failed: database is locked`，说明当时靠 SQLite 兜底而非单实例约束。
- actual_output: 工位同一断言 → `SUMMARY: 13 ok, 0 failed`（AT-001-GREEN.log）。loser 输出 `freely-db daemon already running (singleton lock held)`。
- evidence_file: docs/B2-docs/runtime/concurrency/raw-20261103T132622Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 启动锁组 source 真实 `freely` 后调用 `acquire_project_start_lock_or_wait`，用四种锁目录状态验证：①刚 `mkdir` 未写 state（TOCTOU 窗口）②age=3600s 无 state ③活 owner（真实 `bash -c 'source freely; sleep 30'`）④PID 复用（`sleep 30`，cmdline 不含 freely）。DB 组用两个真实子进程同时 `freely_db_manager.py start --project <tmp> --foreground`，3s 后统计存活进程、探测 socket、比对 pid 文件与存活 pid、检查 loser 文案。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github` 出 `/tmp/r19-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r19-base` 运行。

## End-to-End
- acceptance_target: 并发双启动的真实进程级行为
- testing_layer: end-to-end
- target_environment: 真实子进程 + 临时项目 + `/tmp/freely-db-*` 隔离路径
- required_evidence: AT-001（DB 组 4 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py

## Unit
- acceptance_target: 锁目录 age 判定与 cmdline owner 判定
- testing_layer: unit
- target_environment: fix/raw-20261103T132622Z-flock-startup-lock
- required_evidence: AT-001（启动锁组 4 项 + 静态 5 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py

## Integration
- acceptance_target: 既有生命周期与门禁能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-test-gate-record
2. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
3. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
4. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 测试用隔离临时项目与 `/tmp/freely-db-<hash>` 路径，不触碰真实 `.freely/run` 与真实 daemon；每个用例结束 kill 进程并清理 pid/socket。真实环境只做只读核对（`freely doctor` / `install-state-check`）。
- real_environment_reason: 该缺陷的触发条件是「两个真实进程同时启动」，只能在真实子进程层面复现；本机 `ps` 被沙箱禁用，AT 对 `ps` 不可读场景做了保守断言（不误杀活锁），并在 RED/GREEN 日志中标注。
