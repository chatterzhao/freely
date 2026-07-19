# Pre-Tests: agent lifecycle
- issue_id: I-20260719T123039Z-A
## Acceptance Items
### acceptance-1
- id: AT-001 / requirement: stale NULL行已清理 / testing_layer: unit / evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-lifecycle-test/raw-20260719T123039Z/verification/test-evidence/acceptance-1.log
- test_command: test-agent-lifecycle.sh Test 1 / expected_output: PASS / red-green-status: green / status: pass
- red_how: 有3行worker_id=NULL的stale行
### acceptance-2
- id: AT-002 / requirement: next_free返回正确空闲实例 / testing_layer: unit / evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-lifecycle-test/raw-20260719T123039Z/verification/test-evidence/acceptance-2.log
- test_command: test-agent-lifecycle.sh Test 2 / expected_output: PASS / red-green-status: green / status: pass
- red_how: worker_id全是NULL, next_free始终返回worker_01(无法检测占用)
### acceptance-3
- id: AT-003 / requirement: assign→verify→release完整lifecycle / testing_layer: unit / evidence_level: real_env
- artifact_ref: docs/B2-docs/config/agent-lifecycle-test/raw-20260719T123039Z/verification/test-evidence/acceptance-3.log
- test_command: test-agent-lifecycle.sh Test 3 / expected_output: PASS / red-green-status: green / status: pass
- red_how: agent_assign可能因L3拒绝而静默失败
## Unit: AT-001~003 / target_environment: fix-raw-20260719T123039Z-agent-lifecycle-test / not_applicable_reason: covered_by_more_realistic_required_surface / replacement_evidence: AT-001~003
## Integration: daemon运行后agent_working有正确worker_id / target_environment: test-pre-merge-20260719T123039Z-agent-lifecycle-test / not_applicable_reason: covered_by_more_realistic_required_surface
## End-to-End: post-merge daemon / target_environment: develop merge chain / not_applicable_reason: covered_by_more_realistic_required_surface
## Real-Environment: real_environment_status: pass / real_environment_reason: cleanup完成+test通过
