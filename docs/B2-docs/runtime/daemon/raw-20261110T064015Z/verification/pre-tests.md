# Pre-Tests: 派发 CAS 幂等 + SSE watchdog 单实例所有权
- issue_id: I-20261110T064015Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 派发链四层贯通可选 `expected_state` CAS（CLI 登记参数并 fail-closed → server 409 → DB `WHERE state = ?` → 启动 worker 前抢占），且 SSE 监督者不嵌套启动 consumer、三处 pid 写入有 flock 互斥
- acceptance_target: 同一 `submitted` 任务只能被一个派发器抢占；同一时刻只有一个 shell SSE consumer 与一个 python watchdog 持有 pid
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 出的隔离基线快照 / 工位真源；真实 `freely_db_manager.py` handler 跑在隔离临时 SQLite；真实 `a2a_task.py` CLI 通过 `A2A_REMOTE_URL` 指向本地 stub REST server；真实 `runtime/freely` 被 source 后由两个并发 bash 进程抢同一 pid 文件。不访问 GitHub/Gitee、不碰真实 `.freely/freely.db`、不启动真实 A2A Server / daemon、不派发真实 agent、不杀本机进程
- required_evidence: 11 静态 + 4 DB 行为 + 3 CLI 行为 + 2 并发 pid = 20 项全 GREEN；基线 RED `2 ok / 18 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
- test_command: python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok / 18 failed（2 项 PASS 是守卫：无条件普通 update 仍生效、legacy `--status launched` 仍映射 working）
- actual_RED_output: develop `6715a67a2` 基线快照注入最终版 AT-001 → `SUMMARY: 2 ok, 18 failed`（AT-001-RED.log）。关键：`CLI PATCH body carries expected_state=submitted` FAIL（参数被 `parse_known_args()` 吞掉）、`first CAS wins` / `second CAS loses` FAIL（handler 把 `expected_state` 当列名）、`exactly one concurrent claim succeeds` FAIL（无 claim helper）。
- actual_output: 工位同一断言 → `SUMMARY: 20 ok, 0 failed`（AT-001-GREEN.log）；含 `first CAS wins (affected=1)`、`second CAS loses (affected=0)`、`409 conflict makes the CLI fail closed`、`pid file records the winning owner only`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T064015Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组逐层断言接线与顺序（派发循环内 `--expected-state "submitted"` 的偏移必须早于 `launch_worker_from_manager_prompt_if_needed`；ensure-watch 段不得再出现嵌套 `bash ... --watch` 与 `echo "$$" > pid`）。行为 A 用 `importlib` 加载真实 DB daemon 模块、构造只有 `a2a_tasks` 三列的隔离库，连续两次 `submitted → working` CAS，断言 affected 1 → 0，另守卫生效的普通 update 与错配拒绝。行为 B 用 `ThreadingHTTPServer` stub 接住真实 CLI 的 PATCH，断言 body 带 `expected_state=submitted`，再让 stub 返回 409 `state_conflict`，断言 CLI 非零退出且 stdout 含 conflict。行为 C 由两个并发 `bash -c 'source runtime/freely; sse_watchdog_claim_pid ...'` 抢同一 pid 文件，成功者保持存活 2 秒，断言恰好一个 rc=0 且 pid 文件内容等于成功者 pid。
- red_how: `git archive develop | tar -x -C /tmp/r23j-base`，**只**拷最终版 AT-001 进基线，以 `--source-dir /tmp/r23j-base` 运行。基线不含任何实现改动。
- implementation_findings: GREEN 首轮 `18 ok / 2 failed` 暴露 DB handler 的参数顺序 bug（`expected_state` 被 append 到 `task_id` 之前，SQL 变成 `task_id=submitted AND state=T1`）；修正为 `values = SET值 + [now, task_id] + [expected_state]` 后全绿。行为断言抓到了静态断言抓不到的真实错误。

## End-to-End
- acceptance_target: 真实 CLI → REST → DB handler 的 CAS 链，以及两个并发 watchdog 的 pid 所有权
- testing_layer: end-to-end
- target_environment: 隔离 SQLite + 本地 stub REST + 临时 pid 文件
- required_evidence: AT-001（9 项行为）+ `bin/test-all --ci` 实跑
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
2. bin/test-all --ci

## Unit
- acceptance_target: 四层接线与顺序的静态契约
- testing_layer: unit
- target_environment: fix/raw-20261110T064015Z-dispatch-cas-sse
- required_evidence: AT-001（11 项静态）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py

## Integration
- acceptance_target: 既有并发/DB/输入边界/副本/标题回归不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 11 项回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
2. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
3. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
4. python3 docs/system/workspace/scripts/tests/test-reviewer-contract.py
5. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
6. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py
7. python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py
8. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
9. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
10. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
11. bash docs/system/workspace/scripts/tests/test-materialize-h1 all
12. python3 bin/check-state-file-sources
13. bin/check-state-file-keys
14. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 缺陷只在「真实 Python 解释器加载真实 daemon handler / 真实 CLI 发 HTTP / 真实 bash source + flock」时暴露。夹具全部指向隔离临时目录，A2A Server 用本地 stub 而非真 daemon；不访问平台、不碰真实 `.freely/freely.db`、不派发真实 worker、不启动或杀死本机 watchdog 进程。develop 基线只读用于 RED 对照。
- real_environment_reason: AT-001 RED `2 ok / 18 failed` → GREEN `20 ok / 0 failed`；11 项回归全绿；`bin/test-all --ci` `7 ok / 0 failed` 且确实执行新 AT；`bin/test-all`（local）`10 ok / 1 failed`，唯一失败是既有 `test-github-label-autocreate.py`，develop 基线同样失败，非本轮引入。
