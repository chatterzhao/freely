# Pre-Tests: execution-network 族迁移到安全协议
- issue_id: I-20261110T081029Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 真实 `persist_execution_network_state` 不再插值 heredoc、两处读者不再 source；普通值往返且 launch-block 判定成立；落盘为 TAB+JSON；旧格式兼容且注入文本不执行；恶意值逐字节且不执行；换行值被拒绝；全局状态 source 计数 54→52；耦合测试改为协议断言
- acceptance_target: 把第二族状态文件接入安全协议，同时让「逐族迁移」这套流程可持续（不互相拖红）
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `runtime/freely`（被 source）+ 真实 `state_file.py` CLI + 临时项目目录 `.freely/run/`；develop HEAD 基线快照对比
- required_evidence: 5 静态 + 6 行为共 11 项全 GREEN；基线 RED `4 ok / 7 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-state-family-execution-network.py
- test_command: python3 docs/system/workspace/scripts/tests/test-state-family-execution-network.py
- expected_output: SUMMARY: 11 ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok / 7 failed（3 条静态迁移断言 + lint 计数 + 耦合测试格式断言 + 落盘格式 + 注入 PoC 失败；4 项 PASS 是守卫：普通往返、旧格式可读、协议模块自身的恶意值/换行行为）
- actual_RED_output: develop `9038a2547` 基线快照注入最终版 AT-001 → `SUMMARY: 4 ok, 7 failed`（AT-001-RED.log）。关键证据：`legacy injected text is read as data, not executed (marker=True)` —— 旧实现 `source` 真的执行了 `$(touch marker)`。
- actual_output: 工位同一断言 → `SUMMARY: 11 ok, 0 failed`（AT-001-GREEN.log）；`boundary lint passes and global state sources dropped below 54 (got 52, rc=0)`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T081029Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组断言写入块无 `cat >` 且含 `--kv`/`STATE_FILE_PY`、两处读者块无 `source "$state_file"` 且含 `values`、lint 计数严格低于 54、耦合测试不再 grep 旧格式而走协议。行为组 source 真实 `freely`、设置 `PROJECT_ROOT` 到临时项目，调用真实函数：①写 4 个普通值后 `execution_network_launch_block_active` 返回 0 ②落盘含 `EXECUTION_NETWORK_REASON\t"` ③旧格式 `KEY=value` 仍可读且 block 判定成立 ④旧格式 `$(touch marker)` 不创建 marker ⑤新格式写含 `"`/`$()`/反引号的值读回逐字节且不创建 marker ⑥`values` 对含换行值返回非零并报 newline。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23d-base`，**只**拷最终版 AT-001，以 `--source-dir /tmp/r23d-base` 运行。

## End-to-End
- acceptance_target: shell ↔ python 协议边界的真实行为
- testing_layer: end-to-end
- target_environment: 真实 `freely` 被 source + 临时项目目录
- required_evidence: AT-001（行为 6 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-family-execution-network.py

## Unit
- acceptance_target: 迁移静态契约与边界计数
- testing_layer: unit
- target_environment: fix/raw-20261110T081029Z-migrate-state-family-2
- required_evidence: AT-001（静态 5 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-family-execution-network.py

## Integration
- acceptance_target: 既有协议、前两族、runtime 能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py
2. python3 docs/system/workspace/scripts/tests/test-state-family-cooldown.py
3. bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification
4. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
5. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
6. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
7. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
8. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
9. python3 bin/check-state-file-sources
10. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 所有状态读写在临时项目 `.freely/run/` 内进行，PoC 的 `touch` 只作用于临时目录；不访问平台、不碰主仓 `.freely/`。
- real_environment_reason: 缺陷位于 shell ↔ python 边界，必须 source 真实 `freely` 才能验证；耦合回归 + 两族 AT + 5 个相关测试 + `test-all --ci` + lint 全绿，确认改写未影响 runtime。
