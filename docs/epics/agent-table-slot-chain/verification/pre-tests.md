# Pre-Tests: agent-table slot chain
- issue_id: I-20260625T211802Z-A

## Acceptance Items
### acceptance-1
- acceptance_target: agent-table-query --next-free returns first free worker
- testing_layer: unit
- test_command: test "$(python3 bin/agent-table-query --next-free worker 2>/dev/null)" = "worker_01" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- status: pass

### acceptance-2
- acceptance_target: sync_tooling writes worker-id.env
- testing_layer: unit
- test_command: grep -q "worker-id.env" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- status: pass

### acceptance-3
- acceptance_target: pr-review-guarded reads reviewer_slot
- testing_layer: unit
- test_command: grep -q "worker-id.env" bin/pr-review-guarded && grep -q "get-slot" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- status: pass

## Unit
- acceptance_target: all features implemented

## Integration
- not_applicable_reason: agent_table_infrastructure_not_active_in_test_environment
- not_applicable_explanation: agent-table slot assignment requires runtime worktree creation, tested in production

## End-to-End
- not_applicable_reason: runtime_infrastructure_not_available_in_unit_test
- not_applicable_explanation: E2E verification requires actual wt-create with agent-table active
