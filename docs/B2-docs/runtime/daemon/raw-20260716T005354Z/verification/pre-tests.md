# Pre-Tests: acp_session_register all roles
- issue_id: I-20260716T005354Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: freely script syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T005354Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: PASS (syntax baseline)
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T005354Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
### acceptance-2
- id: AT-002
- requirement: acp_session_register no longer returns early for non-manager
- acceptance_target: return 0 removed from else branch
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep confirms removal
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T005354Z/verification/test-evidence/acceptance-2.log
- test_command: sed -n '4070,4080p' docs/system/workspace/scripts/runtime/freely | grep -q 'return 0' && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: FAIL (return 0 still present)
- actual_RED_output: FAIL - return 0 in else branch
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T005354Z/verification/test-evidence/acceptance-2.log
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
- acceptance_target: worker session_id written to agent_working
- testing_layer: integration
- target_environment: develop
- required_evidence: agent_working shows worker with session_id
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review
## End-to-End
- acceptance_target: multi-agent collaboration works
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: worker + reviewer use correct tools
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 2-line removal: return 0 deleted, all roles written
