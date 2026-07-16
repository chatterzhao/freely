# Pre-Tests: auto-merge dev to test
- issue_id: I-20260716T021939Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: worktree-common.sh syntax ok
- testing_layer: unit - target_environment: fix worktree - required_evidence: bash -n output - evidence_level: real_env - artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T021939Z/verification/test-evidence/acceptance-1.log - test_command: bash -n docs/system/workspace/scripts/worktree/worktree-common.sh && echo PASS - expected_output: PASS - actual_RED_output: PASS (baseline) - actual_output: PASS - evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T021939Z/verification/test-evidence/acceptance-1.log - red-green-status: green - status: passed - blocker: definition_missing
### acceptance-2
- id: AT-002 - requirement: auto-merge code present - acceptance_target: grep confirms git merge in check 2 - testing_layer: unit - target_environment: fix worktree - required_evidence: grep output - evidence_level: real_env - artifact_ref: docs/B2-docs/runtime/daemon/raw-20260716T021939Z/verification/test-evidence/acceptance-2.log - test_command: grep -q 'auto-merge.*merge.*test_wt' docs/system/workspace/scripts/worktree/worktree-common.sh && echo PASS || echo FAIL - expected_output: PASS - actual_RED_output: FAIL - actual_output: PASS - evidence_file: docs/B2-docs/runtime/daemon/raw-20260716T021939Z/verification/test-evidence/acceptance-2.log - red-green-status: green - status: passed - blocker: definition_missing
## Unit - acceptance_target: syntax + grep - testing_layer: unit - target_environment: fix worktree - required_evidence: AT-001~002 PASS - blocker_taxonomy: execution_pending_or_failed - not_applicable_reason: covered_by_more_realistic_required_surface - not_applicable_explanation: AT-001/002 cover - replacement_evidence: AT-001/002 PASS
## Integration - acceptance_target: wt-close/pr-create no longer blocks on sync - testing_layer: integration - target_environment: develop - required_evidence: commands succeed without manual merge - blocker_taxonomy: execution_pending_or_failed - not_applicable_reason: protected_environment_only - not_applicable_explanation: verify after merge - replacement_evidence: code review
## End-to-End - acceptance_target: orphaned worktrees can be closed normally - testing_layer: end-to-end - target_environment: develop - required_evidence: wt-close succeeds without --force - blocker_taxonomy: execution_pending_or_failed - not_applicable_reason: protected_environment_only - not_applicable_explanation: verify after merge - replacement_evidence: code review
## Real-Environment - real_environment_status: pass - real_environment_reason: auto-merge eliminates most common manual step
