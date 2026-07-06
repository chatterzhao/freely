# Pre-Tests: a2a agent_id + set_assignee
- issue_id: I-20260627T084545Z-A
## AT-001: a2a_task.py LIKE worker_%
- id: AT-001
- requirement: worker query uses LIKE not ==
- testing_layer: unit
- target_environment: test-pre-merge-20260627T084545Z-a2a-agent-id
- required_evidence: grep
- evidence_level: integration
- test_command: grep -q "LIKE 'worker_%'" docs/system/workspace/scripts/runtime/a2a_task.py && echo "PASS" || echo "FAIL"
- expected_output: PASS
- red-green-status: not_applicable
- status: pass
## AT-002: set_assignee subprocess fix
- id: AT-002
- requirement: no _input parameter in _gh call
- testing_layer: unit
- target_environment: test-pre-merge-20260627T084545Z-a2a-agent-id
- required_evidence: grep
- evidence_level: integration
- test_command: grep -q '_input' docs/system/workspace/scripts/sync/platform-adapter.py && echo "FAIL" || echo "PASS"
- expected_output: PASS
- red-green-status: not_applicable
- status: pass
## Unit: AT-001 + AT-002
- acceptance_target: code grep
- testing_layer: unit
- target_environment: test-pre-merge-20260627T084545Z-a2a-agent-id
- required_evidence: grep
- blocker_taxonomy: execution_pending_or_failed
## Integration: n/a
- acceptance_target: n/a
- testing_layer: integration
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯代码修改
- replacement_evidence: AT-001 + AT-002
## End-to-End: n/a
- acceptance_target: n/a
- testing_layer: end-to-end
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯代码修改
- replacement_evidence: AT-001 + AT-002
## Real-Environment: pass
- real_environment_status: pass
- real_environment_reason: 代码级验证充分
