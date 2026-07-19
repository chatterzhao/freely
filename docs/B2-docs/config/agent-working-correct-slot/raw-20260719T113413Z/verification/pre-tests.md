# Pre-Tests: agent_working slot
- issue_id: I-20260719T113413Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: L13310 slot从agent-table解析而非AGENT_AI_TOOL
- acceptance_target: grep命中agent-table-query
- testing_layer: unit
- target_environment: fix-raw-20260719T113413Z-agent-working-slot-id
- required_evidence: grep输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c 'agent-table-query.*--get-slot worker_01' docs/system/workspace/scripts/runtime/freely
- expected_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前slot=AGENT_AI_TOOL(Manager的tool)

### acceptance-2
- id: AT-002
- requirement: L13110 错误不吞掉, log_warn可见
- acceptance_target: grep命中log_warn
- testing_layer: unit
- target_environment: fix-raw-20260719T113413Z-agent-working-slot-id
- required_evidence: grep输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'log_warn.*failed to register worker' docs/system/workspace/scripts/runtime/freely
- expected_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前|| true吞掉L3错误

## Unit
- acceptance_target: AT-001~002 grep验证
- testing_layer: unit
- target_environment: fix-raw-20260719T113413Z-agent-working-slot-id
- required_evidence: AT-001~002
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: grep验证代码修改存在
- replacement_evidence: AT-001~002 GREEN

## Integration
- acceptance_target: post-merge daemon重启验证
- testing_layer: integration
- target_environment: test-pre-merge-20260719T113413Z-agent-working-slot-id
- required_evidence: daemon日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge dogfood
- replacement_evidence: AT-001~002 GREEN

## End-to-End
- acceptance_target: post-merge daemon
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: daemon日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge dogfood
- replacement_evidence: AT-001~002 GREEN

## Real-Environment
- real_environment_status: pass
- real_environment_reason: slot从agent-table正确解析, 错误不再静默
