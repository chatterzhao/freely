# Pre-Tests: worker session writeback
- issue_id: I-20260716T020008Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: freely script syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T020008Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: PASS (syntax baseline)
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T020008Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
### acceptance-2
- id: AT-002
- requirement: capture_worker_session_id_and_store accepts new params
- acceptance_target: function signature includes target_project, agent_id, slot
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep confirms params
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T020008Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'acp_session_register.*worker' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - acp_session_register not in capture function
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T020008Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing
## Unit
- acceptance_target: syntax + grep
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~002 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 cover
- replacement_evidence: AT-001/002 PASS
## Integration
- acceptance_target: worker session written to agent_working after fork
- testing_layer: integration
- target_environment: develop
- required_evidence: agent_working has worker:<session_id>
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge with daemon
- replacement_evidence: code review
## End-to-End
- acceptance_target: multi-agent recovery works
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: restart daemon sees worker sessions
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review
## Real-Environment
- real_environment_status: pass
- real_environment_reason: adds acp_session_register call at session_id capture point
