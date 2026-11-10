# Pre-Tests: 状态文件安全协议（第一阶段）
- issue_id: I-20261110T060553Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 旧格式 `source` 的注入 PoC 真实执行；新协议对含双引号/换行/tab/`$()`/反引号的值逐字节 round-trip 且不执行；未知键读写都拒绝；旧格式读回原样不展开；`to-shell` 生成惰性赋值；边界 lint 冻结 55 处 source 且禁止 eval/exec
- acceptance_target: 状态文件协议有单一所有者与可机械验证的边界，为逐组迁移提供安全底座
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `state_file.py` + 真实 bash 子进程（PoC 与 to-shell 回读）+ 临时目录；develop HEAD 基线快照对比
- required_evidence: 2 静态 + 7 行为共 9 项全 GREEN；基线 RED `1 ok / 7 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-state-file-protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py
- expected_output: SUMMARY: 9 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok / 7 failed（安全模块与 lint 不存在；round-trip/不注入/未知键/兼容/to-shell 全部无法执行。1 项 PASS 是注入 PoC——它必须真的执行，否则测试只是 grep）
- actual_RED_output: develop `ea9f5b38c` 基线快照注入最终版 AT-001 → `SUMMARY: 1 ok, 7 failed`（AT-001-RED.log）。PoC 创建 marker 文件成功。
- actual_output: 工位同一断言 → `SUMMARY: 9 ok, 0 failed`（AT-001-GREEN.log）；恶意值含 `"`、`\n`、`\t`、`$(...)`、反引号均逐字节相等且 marker 未创建。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T060553Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言安全模块含 `read_state`/`write_state`/`to_shell`/`ALLOWED_KEYS` 且无 `eval(`/`exec(`/`os.system`/`subprocess`，并实跑边界 lint。行为组：①`LAST_EXIT_REASON="$(touch marker)"` 经 `source` 真的创建 marker ②新 writer/reader 对恶意值逐字节相等 ③读新格式不创建 marker ④写/读未知键各抛 StateFileError ⑤旧格式 `$HOME $(id) \`whoami\`` 读回原样 ⑥`to-shell` 输出被 source 后不执行且值完整。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23b-base`，**只**把最终版 AT-001 拷入快照 tests 目录（不拷实现），以 `--source-dir /tmp/r23b-base` 运行。

## End-to-End
- acceptance_target: 真实 bash source 与协议 round-trip
- testing_layer: end-to-end
- target_environment: 真实 bash 子进程 + 临时状态文件
- required_evidence: AT-001（行为 7 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py

## Unit
- acceptance_target: 安全模块静态契约与边界 lint
- testing_layer: unit
- target_environment: fix/raw-20261110T060553Z-state-file-protocol
- required_evidence: AT-001（静态 2 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py

## Integration
- acceptance_target: 既有 runtime / 契约 / 物化能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
2. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
3. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
4. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
5. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
6. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
7. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 本轮**未改** `runtime/freely` 任何一行，只新增 `state_file.py` 与 lint；PoC 与 to-shell 都在临时目录执行，不访问平台、不碰真实 `.freely/run/`。
- real_environment_reason: 旧格式的注入只能在真实 bash `source` 下证明；新协议必须由真实读写链路验证。6 个相关测试 + `bin/test-all --ci` + 边界 lint 全绿，说明新增文件未影响既有 runtime。
