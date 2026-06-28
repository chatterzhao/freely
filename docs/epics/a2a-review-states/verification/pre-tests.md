# Pre-Tests: A2A review states
- issue_id: I-20260626T025748Z-A
## Acceptance Items
### acceptance-1
- test_command: grep -q "freely-review" docs/system/workspace/agents/manager-agent.md && grep -q "worker_in_review" docs/system/workspace/a2a/exit-kind-mapping.md && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- status: pass
## Unit
- acceptance_target: docs correct
## Integration
- not_applicable_reason: documentation_change_no_runtime_behavior
## End-to-End
- not_applicable_reason: requires_acp_bridge_daemon
