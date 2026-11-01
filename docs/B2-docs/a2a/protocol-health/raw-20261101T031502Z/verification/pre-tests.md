# pre-tests：report/attention + prompt manifest

> B2 写入 pending；RED 后 red；GREEN 后 green。

## Unit
- acceptance_target: report/attention/batch 校验与存储
- testing_layer: unit
- target_environment: feature-local
- required_evidence: unittest OK
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-agent-protocol.py。
2. 运行 test-prompt-manifest.py。

### acceptance-1：report 六态
- id: PC-1
- requirement: 六态合法；非法 state 拒绝；summary 必填
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-2：attention 单问题
- id: PC-2
- requirement: needed=true 只能一个问题且 target_role 必填；false 时字段为空
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-3：批量决策幂等
- id: PC-3
- requirement: trigger_id 唯一；每条 reason 必填；重复不新增
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-4：manifest prefix
- id: PC-4
- requirement: 11 段 marker；tail 变化 prefix hash 不变；无 marker 退化为 full_prompt
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/prompt_manifest.py
- test_command: python3 docs/system/workspace/scripts/tests/test-prompt-manifest.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-prompt-manifest.log
- expected_output: OK
- actual_output: pending

## Integration
- acceptance_target: CLI + run-acp-prompt 日志
- testing_layer: integration
- target_environment: feature-local + temp project
- required_evidence: CLI JSON + JSONL
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-a2a-report-cli.py。
2. 运行 test-prompt-manifest-integration.py。

### acceptance-5：a2a-report/decide CLI
- id: PC-5
- requirement: record/list 可用，数据落 agent_reports/agent_decisions
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/a2a-report
- test_command: python3 docs/system/workspace/scripts/tests/test-a2a-report-cli.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-a2a-report-cli.log
- expected_output: OK
- actual_output: pending

### acceptance-6：run-acp-prompt 记录 manifest
- id: PC-6
- requirement: 调用 manifest helper 后 JSONL 有记录；无 marker 仍有 full_prompt
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/run-acp-prompt.py
- test_command: python3 docs/system/workspace/scripts/tests/test-prompt-manifest-integration.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-prompt-manifest-integration.log
- expected_output: OK
- actual_output: pending

## End-to-End
- acceptance_target: report→store→list；manifest→JSONL
- testing_layer: end_to_end
- target_environment: temp project + temp DB
- required_evidence: CLI output
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-a2a-report-cli.py。
2. 运行 test-prompt-manifest-integration.py。

### acceptance-7：端到端
- id: PC-7
- requirement: 一条 ready report + 一条 ignore decision 可查询；manifest 可对照
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/a2a-report
- test_command: python3 docs/system/workspace/scripts/tests/test-a2a-report-cli.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-a2a-report-cli.log
- expected_output: OK
- actual_output: pending

## Real-Environment
- real_environment_status: pass
- real_environment_reason: temp project 真实 SQLite/CLI 跑 a2a-report record/list 与 manifest JSONL；见 test-evidence/real-environment.log。

## Acceptance Items
### acceptance-1
- id: PC-1
- requirement: report 六态
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-2
- id: PC-2
- requirement: attention 单问题
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-3
- id: PC-3
- requirement: 批量决策幂等
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/agent_protocol.py
- test_command: python3 docs/system/workspace/scripts/tests/test-agent-protocol.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-agent-protocol.log
- expected_output: OK
- actual_output: pending

### acceptance-4
- id: PC-4
- requirement: manifest prefix
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/prompt_manifest.py
- test_command: python3 docs/system/workspace/scripts/tests/test-prompt-manifest.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-prompt-manifest.log
- expected_output: OK
- actual_output: pending

### acceptance-5
- id: PC-5
- requirement: a2a-report/decide CLI
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/a2a-report
- test_command: python3 docs/system/workspace/scripts/tests/test-a2a-report-cli.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-a2a-report-cli.log
- expected_output: OK
- actual_output: pending

### acceptance-6
- id: PC-6
- requirement: run-acp-prompt manifest 日志
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/system/workspace/scripts/runtime/run-acp-prompt.py
- test_command: python3 docs/system/workspace/scripts/tests/test-prompt-manifest-integration.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-prompt-manifest-integration.log
- expected_output: OK
- actual_output: pending

### acceptance-7
- id: PC-7
- requirement: 端到端
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: bin/a2a-report
- test_command: python3 docs/system/workspace/scripts/tests/test-a2a-report-cli.py
- actual_output: OK
- evidence_file: docs/B2-docs/a2a/protocol-health/raw-20261101T031502Z/verification/test-evidence/test-a2a-report-cli.log
- expected_output: OK
- actual_output: pending
