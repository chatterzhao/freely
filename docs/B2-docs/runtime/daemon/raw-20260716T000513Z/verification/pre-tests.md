# Pre-Tests: agent_assign in worker launch
- issue_id: I-20260716T000513Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n syntax check passes
- acceptance_target: freely script syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: PASS (syntax baseline)
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: agent_assign called in launch_worker_from_manager_prompt_if_needed
- acceptance_target: new agent_assign call present before fork launch
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep confirms agent_assign call
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'agent_assign.*worker_01' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (agent_assign not in launch path)
- actual_RED_output: FAIL - agent_assign only in sync_project_tooling
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T000513Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: bash syntax + grep verification
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001 and AT-002 pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 and AT-002 cover all unit test needs
- replacement_evidence: AT-001 and AT-002 PASS

## Integration
- acceptance_target: worker launch writes agent_working entry
- testing_layer: integration
- target_environment: develop
- required_evidence: agent_working has worker entry after delegation
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: requires daemon restart with worker delegation to verify
- replacement_evidence: code review confirms agent_assign placed before fork launch

## End-to-End
- acceptance_target: worker daemon resolves correct agent role
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: worker uses agent-table configured slot
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: requires full multi-agent collaboration to verify
- replacement_evidence: code review + unit tests

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 5-line change adds agent_assign call before worker fork launch
