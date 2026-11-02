# Pre-Tests: 副本观测三态化与债账本
- issue_id: I-20261102T113816Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: transport 读取异常记为 unknown 而不是 error，且不得变成 missing
- acceptance_target: 一个平台读取失败时 receipt 仍能区分“读不到”与“确实没有”
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T113816Z-replica-gate-unknown-vs-missing
- required_evidence: FakeHandler 抛异常后 discover_raw_replicas 的 status 与 error 文本
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- expected_output: OK
- expected_RED_output: AssertionError: 'error' != 'unknown'
- actual_RED_output: AssertionError: 'error' != 'unknown' — {'status': 'error', 'error': 'raw search failed'}
- actual_output: OK —— status=unknown，error 保留 502 proxy 原文
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/verification/test-evidence/test-raw-replica-degraded-RED.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-2
- id: AT-002
- requirement: 瞬时失败在重试预算内自愈，不产生 degraded
- acceptance_target: 前两次抛异常、第三次成功时 status=ok 且调用次数 ≥ 3
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T113816Z-replica-gate-unknown-vs-missing
- required_evidence: 重试次数与最终状态
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- expected_output: OK
- expected_RED_output: AssertionError: 'error' != 'ok'
- actual_RED_output: AssertionError: 'error' != 'ok' — 无重试，第一次异常即返回
- actual_output: OK —— calls=3，status=ok
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/verification/test-evidence/test-raw-replica-degraded-RED.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-3
- id: AT-003
- requirement: 默认语义不变（unknown 阻塞）；allow_degraded 才放行并输出 debt
- acceptance_target: 同一输入下 decision 分别为 block 与 allow_degraded，debt 精确列出平台与原因
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T113816Z-replica-gate-unknown-vs-missing
- required_evidence: 两种开关下的 ok/decision/debt
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/lifecycle/raw_reconciliation.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- expected_output: OK
- expected_RED_output: TypeError: reconcile() got an unexpected keyword argument 'allow_degraded'
- actual_RED_output: TypeError: reconcile() got an unexpected keyword argument 'allow_degraded'
- actual_output: OK —— block / allow_degraded，debt=[{platform: gitee, reason: 502}]
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/verification/test-evidence/test-raw-replica-degraded.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-4
- id: AT-004
- requirement: 事实类诊断（missing / diverged / 全平台不可读）在降级模式下仍然阻塞
- acceptance_target: allow_degraded 不改变任何事实判定
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T113816Z-replica-gate-unknown-vs-missing
- required_evidence: 三个反向用例均 ok=False 且 decision=block
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/lifecycle/raw_reconciliation.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
- expected_output: OK
- expected_RED_output: TypeError: reconcile() got an unexpected keyword argument 'allow_degraded'
- actual_RED_output: TypeError: reconcile() got an unexpected keyword argument 'allow_degraded'
- actual_output: OK —— missing / content_diverged / all-unknown 三例均 block
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/verification/test-evidence/test-raw-replica-degraded.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-5
- id: AT-005
- requirement: gate 接线正确：严格模式拒绝 unknown，降级模式放行并给出 debt，missing 始终拒绝
- acceptance_target: 四次真实 gate 调用的退出码与 decision 符合约定
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix worktree with configured platforms github,gitee
- required_evidence: gate-allow / gate-block-unknown / gate-allow-degraded / gate-block-missing 四份 receipt
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py
- test_command: python3 docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py --project . --raw-key 20261102T113816Z
- expected_output: 严格 rc=0；unknown rc=1；allow-degraded rc=0；missing rc=1
- expected_RED_output: gate 不接受 --allow-degraded（unrecognized arguments）
- actual_RED_output: unrecognized arguments: --allow-degraded
- actual_output: rc 依次为 0 / 1 / 0 / 1，decision 为 allow / block / allow_degraded / block
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261102T113816Z/verification/test-evidence/gate-allow-degraded.json
- red-green-status: green
- status: passed
- blocker: ""
