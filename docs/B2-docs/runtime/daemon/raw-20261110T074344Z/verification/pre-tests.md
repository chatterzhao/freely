# Pre-Tests: cooldown 族迁移到安全协议
- issue_id: I-20261110T074344Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 真实 `_read/_write_cooldown_state` 不再 source 状态文件；普通值往返；落盘为 TAB+JSON；旧 KEY=value 兼容且注入文本不执行；恶意值逐字节且不执行；换行值被拒绝；全局状态 source 计数 55→54
- acceptance_target: 把协议从「存在」变成「被使用」，给出可复制的逐族迁移样板
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `runtime/freely`（被 source）+ 真实 `state_file.py` CLI + 临时项目目录 `.freely/run/`；develop HEAD 基线快照对比
- required_evidence: 2 静态 + 6 行为共 8 项全 GREEN；基线 RED `2 ok / 6 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-state-family-cooldown.py
- test_command: python3 docs/system/workspace/scripts/tests/test-state-family-cooldown.py
- expected_output: SUMMARY: 8 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok / 6 failed（2 项 PASS 是守卫：普通值往返、旧格式兼容；6 项 FAIL 含 `marker=True` 两次——旧实现真的执行了注入）
- actual_RED_output: develop `7d455713f` 基线快照注入最终版 AT-001 → `SUMMARY: 2 ok, 6 failed`（AT-001-RED.log）。关键：`legacy injected text ... (marker=True)`、`hostile value ... (marker=True)`。
- actual_output: 工位同一断言 → `SUMMARY: 8 ok, 0 failed`（AT-001-GREEN.log）；`boundary lint ... 55 -> 54 (got 54)`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T074344Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言 cooldown 块内无 `source`、含 `--kv`/`STATE_FILE_PY`，并实跑 lint 断言计数恰为 54。行为组 source 真实 `freely`、设置 `PROJECT_ROOT` 到临时项目，调用真实函数：①普通值 1730000000/7 往返 ②落盘含 `COOLDOWN_SWITCH_AT\t"` ③旧格式 `99/3` 可读 ④旧格式 `$(touch marker)` 不创建 marker ⑤新格式写含 `"`/`$()` 的值读回逐字节且不创建 marker ⑥`values` 对含换行值返回非零并报 newline。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23c-base`，**只**拷最终版 AT-001，以 `--source-dir /tmp/r23c-base` 运行。

## End-to-End
- acceptance_target: shell ↔ python 协议边界的真实行为
- testing_layer: end-to-end
- target_environment: 真实 `freely` 被 source + 临时项目目录
- required_evidence: AT-001（行为 6 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-family-cooldown.py

## Unit
- acceptance_target: 迁移静态契约与边界计数
- testing_layer: unit
- target_environment: fix/raw-20261110T074344Z-migrate-state-family
- required_evidence: AT-001（静态 2 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-family-cooldown.py

## Integration
- acceptance_target: R23.9 协议与既有 runtime 不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py
2. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
3. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
4. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
5. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
6. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 所有状态读写在临时项目 `.freely/run/` 内进行，PoC 的 `touch` 只作用于临时目录；不访问平台、不碰主仓 `.freely/`。
- real_environment_reason: 缺陷位于 shell ↔ python 边界，必须 source 真实 `freely` 才能验证；5 个相关测试 + `test-all --ci` + lint 全绿，确认两函数改写未影响 runtime。
