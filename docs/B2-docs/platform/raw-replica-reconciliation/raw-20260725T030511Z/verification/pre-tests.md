# Pre-Tests: 配置平台 raw 副本一致性
- issue_id: I-20260725T030511Z-A

## Acceptance Items

### AT-001
- requirement: raw-key 比较与单平台唯一匹配稳定
- testing_layer: unit
- target_environment: feature/raw-20260725T030511Z-raw-replica-reconciliation
- required_evidence: 大小写 key 与 empty result 的断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/adapter-reconciliation.log
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
- expected_output: OK
- expected_RED_output: ModuleNotFoundError 或断言失败
- actual_RED_output: "Ran 3 tests in 0.002s FAILED (errors=3) — FileNotFoundError: raw_reconciliation.py 不存在"
- actual_output: "Ran 3 tests in 0.041s OK"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/adapter-reconciliation.log
- red-green-status: green
- status: passed
- blocker: ""
- red_how: "单元测试 test-raw-reconciliation.py，功能未实现（reconciliation module 缺失），执行结果: errors=3"

### AT-002
- requirement: 缺副本、差异、不可达平台 fail-closed，且 receipt 无写副作用
- testing_layer: integration
- target_environment: feature/raw-20260725T030511Z-raw-replica-reconciliation
- required_evidence: 模拟 transport 的 receipt 状态与无 mutation 断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/adapter-reconciliation.log
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
- expected_output: OK
- expected_RED_output: ModuleNotFoundError 或断言失败
- actual_RED_output: "Ran 3 tests in 0.002s FAILED (errors=3) — FileNotFoundError: raw_reconciliation.py 不存在"
- actual_output: "Ran 3 tests in 0.041s OK"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/adapter-reconciliation.log
- red-green-status: green
- status: passed
- blocker: ""
- red_how: "集成测试 test-raw-reconciliation.py，discovery/receipt 接口缺失，执行结果: errors=3"

### AT-003
- requirement: scan 不把 adapter 故障解释为空平台清单
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260725T030511Z-raw-replica-reconciliation
- required_evidence: scan 调用边界的 degraded 结果
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/scan-reconciliation.log
- test_command: python3 docs/system/workspace/scripts/tests/test-command-lifecycle-consumer-boundaries.py
- expected_output: OK
- expected_RED_output: 缺少 degraded 状态断言
- actual_RED_output: "Ran 7 tests FAILED (failures=1) — AssertionError: {} == {}（adapter 故障被空集合化）"
- actual_output: "Ran 7 tests in 0.101s OK"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/verification/test-evidence/scan-reconciliation.log
- red-green-status: green
- status: passed
- blocker: ""
- red_how: "集成测试 test-command-lifecycle-consumer-boundaries.py::test_adapter_failure_is_degraded_not_empty_platform_list，adapter 故障时 get_platform_open_issues 返回 {}，执行结果: AssertionError"
