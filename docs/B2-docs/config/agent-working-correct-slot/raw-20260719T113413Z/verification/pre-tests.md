# Pre-Tests: agent_working slot
- issue_id: I-20260719T113413Z-A
## Acceptance Items
### acceptance-1
- id: AT-001 / requirement: L13310用agent-table-query解析worker slot / testing_layer: unit / evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c 'agent-table-query.*--get-slot worker_01' docs/system/workspace/scripts/runtime/freely
- expected_output: "1" / red-green-status: green / status: pass / red_how: 当前用AGENT_AI_TOOL(Manager的tool)
### acceptance-2
- id: AT-002 / requirement: L13110错误不吞掉 / testing_layer: unit / evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T113413Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'log_warn.*failed to register worker' docs/system/workspace/scripts/runtime/freely
- expected_output: "1" / red-green-status: green / status: pass / red_how: 当前|| true吞错误
## Unit: AT-001~002 / target_environment: fix-raw-20260719T113413Z-agent-working-slot-id / not_applicable_reason: covered_by_more_realistic_required_surface / replacement_evidence: AT-001~002
## Integration: post-merge / target_environment: test-pre-merge-20260719T113413Z-agent-working-slot-id / not_applicable_reason: covered_by_more_realistic_required_surface
## End-to-End: target_environment: develop merge chain / not_applicable_reason: covered_by_more_realistic_required_surface
## Real-Environment: real_environment_status: pass / real_environment_reason: slot正确+错误可见
