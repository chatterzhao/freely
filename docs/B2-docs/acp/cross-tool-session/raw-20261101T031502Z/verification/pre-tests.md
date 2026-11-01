# pre-tests：角色级 harness 选择

> B2 写入时 pending；RED 后 red；GREEN 后 green。

## Unit
- acceptance_target: RoleHarnessConfig 归一化、requirements、validate
- testing_layer: unit
- target_environment: feature-local
- required_evidence: unittest OK + evidence logs
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-harness-config.py，覆盖 validate/apply。
2. 运行 test-harness-role.py，覆盖 --role/requirements。

### acceptance-1：validate 只读
- id: HD-1
- requirement: validate 不写文件，缺失 slot/unknown role 失败
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

### acceptance-2：apply 只改一个 slot
- id: HD-2
- requirement: apply 成功后仅 `{role}_slot` 变化，备份/重读/审计存在
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

### acceptance-3：apply 失败不落盘
- id: HD-3
- requirement: 无效 slot/binary 时文件字节不变
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

## Integration
- acceptance_target: harness-status --role 与 requirements/satisfied
- testing_layer: integration
- target_environment: feature-local + temp project
- required_evidence: JSON assertions
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-harness-role.py。
2. 用 temp agent-table 覆盖 manager/worker/reviewer。

### acceptance-4：--role 过滤
- id: HD-4
- requirement: `--role reviewer` 只返回 reviewer；未知 role 返回 2
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_status.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-role.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-role.log
- expected_output: OK
- actual_output: pending

### acceptance-5：reviewer fork degraded
- id: HD-5
- requirement: reviewer cline 输出 fork=degraded，satisfied=true，degraded 列表含 fork
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_status.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-role.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-role.log
- expected_output: OK
- actual_output: pending

## End-to-End
- acceptance_target: CLI show/validate/apply 全链路
- testing_layer: end_to_end
- target_environment: temp project + temp HOME
- required_evidence: command output + file diff
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-harness-e2e.py。

### acceptance-6：CLI 全链路
- id: HD-6
- requirement: show → validate → apply → status 反射新 slot
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/harness-select
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-e2e.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-e2e.log
- expected_output: OK
- actual_output: pending

## Real-Environment
- real_environment_status: pass
- real_environment_reason: test-pre-merge 工位用真实 agent-table 跑 harness-select validate reviewer（只读），返回 ok；见 test-evidence/real-environment.log。

## Acceptance Items
### acceptance-1
- id: HD-1
- requirement: validate 只读
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

### acceptance-2
- id: HD-2
- requirement: apply 只改一个 slot
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

### acceptance-3
- id: HD-3
- requirement: apply 失败不落盘
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_config.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-config.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-config.log
- expected_output: OK
- actual_output: pending

### acceptance-4
- id: HD-4
- requirement: --role 过滤
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_status.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-role.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-role.log
- expected_output: OK
- actual_output: pending

### acceptance-5
- id: HD-5
- requirement: reviewer fork degraded
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/harness_status.py
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-role.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-role.log
- expected_output: OK
- actual_output: pending

### acceptance-6
- id: HD-6
- requirement: CLI 全链路
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/harness-select
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-e2e.py
- actual_output: OK
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261101T031502Z/verification/test-evidence/test-harness-e2e.log
- expected_output: OK
- actual_output: pending
