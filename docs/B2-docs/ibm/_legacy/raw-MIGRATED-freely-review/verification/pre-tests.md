# Pre-Tests: freely-review
- issue_id: I-20260626T033913Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: agent-table pool expansion correct
- test_command: test $(python3 bin/agent-table-query --list worker 2>/dev/null | wc -l) -eq 10 && test $(python3 bin/agent-table-query --list reviewer 2>/dev/null | wc -l) -eq 11 && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed
### acceptance-2
- acceptance_target: freely-review syntax ok
- test_command: bash -n bin/freely-review && grep -q "caller" bin/freely-review && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed
## Unit
- acceptance_target: basic functionality
## Integration
- not_applicable_reason: agent_table_infrastructure_not_active_in_test_env
## End-to-End
- not_applicable_reason: requires_acp_bridge_daemon_running
