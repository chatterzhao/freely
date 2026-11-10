# Pre-Tests: supervisor 失败退出码 + Python 版本前置
- issue_id: I-20261103T132644Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `will now stop` 分支以非零退出并记录 `exit_kind=degraded_no_recovery`；`bin/freely` 在 exec 前检查 `python3` 存在且 `>= 3.11`，失败时输出含 `Python >= 3.11` 的明确错误
- acceptance_target: 无恢复路径的 workcell 停止能被外层识别为失败；旧 Python 上首错即为版本提示
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 隔离基线 / 工位真源；行为测试用 PATH 前置的 `python3` stub（`version_info` 返回 0/1，`realpath` 透传 argv，其余 exec 真实解释器），不安装旧 Python、不改系统 PATH、不启动 daemon
- required_evidence: 3 静态 + 3 行为 = 6 项全 GREEN；基线 RED `2 ok / 4 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-fail-semantics-preflight.py
- test_command: python3 docs/system/workspace/scripts/tests/test-fail-semantics-preflight.py
- expected_output: SUMMARY: 6 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok / 4 failed（2 项 PASS 是守卫：stub 新版本、真实环境的 `--help`）
- actual_RED_output: develop `502496df1` 基线 + 最终版 AT-001 → `SUMMARY: 2 ok, 4 failed`（AT-001-RED.log）。关键：`supervisor 'will now stop' branch exits non-zero` FAIL、`bin/freely checks Python >= 3.11 before exec` FAIL、`old Python is rejected with a precise message` FAIL（旧入口 rc=0、无版本文案）。
- actual_output: 工位同一断言 → `SUMMARY: 6 ok, 0 failed`（AT-001-GREEN.log）。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261103T132644Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组在 `will now stop` 之后 700 字符窗口内断言 `exit 1` 且无 `exit 0`（注释也避免写出旧值），并断言入口含 `version_info`、`(3, 11)`、`Python >= 3.11`。行为组用 stub 覆盖两条路径：`STUB_PY_OK=0` 断言非零退出 + 文案；`STUB_PY_OK=1` 断言 `--help` rc=0；再以原始 PATH 跑一次真实环境守卫。
- red_how: `git archive develop | tar -x -C /tmp/r25-base`，只注入最终版 AT-001，`--source-dir /tmp/r25-base` 运行。
- implementation_findings: stub 第一版把 realpath 参数位置写成 `$2`，实际 `python3 -c <code> <path>` 的路径在 `$3`，导致守卫项误报失败；修正后 RED 收敛为 2/4，证明「守卫项失败先查夹具、再判产品」。

## End-to-End
- acceptance_target: 真实入口在旧/新 Python 下的行为
- testing_layer: end-to-end
- target_environment: PATH 前置 stub + 真实解释器
- required_evidence: AT-001（3 项行为）+ `bin/test-all --ci`
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-fail-semantics-preflight.py
2. bin/test-all --ci

## Unit
- acceptance_target: 退出码与前置检查的静态接线
- testing_layer: unit
- target_environment: fix/raw-20261103T132644Z-fail-semantics-preflight
- required_evidence: AT-001（3 项静态）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-fail-semantics-preflight.py

## Integration
- acceptance_target: CLI help / 并发 / DB / 派发 / 契约 / wt-create 不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 11 项回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-cli-help-contracts
2. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
3. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
4. python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
5. python3 docs/system/workspace/scripts/tests/test-contract-single-source.py
6. python3 docs/system/workspace/scripts/tests/test-install-state.py
7. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
8. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
9. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-create.py
10. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
11. bash docs/system/workspace/scripts/tests/test-materialize-h1 all
12. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 旧 Python 用 PATH 前置 stub 模拟（只拦截 `-c` 里的 `version_info`/`realpath`，其余交给真实解释器），不安装/不切换系统 Python；不启动 daemon、不写真实日志、不访问平台。
- real_environment_reason: AT-001 RED `2 ok / 4 failed` → GREEN `6 ok / 0 failed`；11 项回归全绿；`bin/test-all --ci` `9 ok / 0 failed` 且执行新 AT；local 模式仅既有 `test-github-label-autocreate.py` 失败（develop 基线同样失败）。
