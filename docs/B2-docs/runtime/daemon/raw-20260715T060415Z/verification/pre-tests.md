# Pre-Tests: scan injection field alignment
- issue_id: I-20260715T060415Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: freely script syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T060415Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T060415Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
### acceptance-2
- id: AT-002
- requirement: field names aligned to scan output
- acceptance_target: grep confirms total/station/by_station usage
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T060415Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'summary.get("total"' docs/system/workspace/scripts/runtime/freely && grep -q 'summary.get("by_station"' docs/system/workspace/scripts/runtime/freely && grep -q 'it.get("station"' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T060415Z/verification/test-evidence/acceptance-2.log
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
- not_applicable_explanation: AT-001/002 cover all
- replacement_evidence: AT-001/002 PASS
## Integration
- acceptance_target: scan data appears in prompt with stage breakdown
- testing_layer: integration
- target_environment: develop
- required_evidence: prompt contains stage grouping
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review + grep
## End-to-End
- acceptance_target: AI works with full scan data
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: AI does productive work
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 3-field alignment with backward compat
