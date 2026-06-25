# Pre-Tests: wt-close consistency
- issue_id: I-20260625T235348Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: consistency check exists
- testing_layer: unit
- required_evidence: grep
- test_command: grep -q "_consistency_check" docs/system/workspace/scripts/worktree/wt-close && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- status: pass

### acceptance-2
- acceptance_target: feature branch case exists
- testing_layer: unit
- required_evidence: grep
- test_command: grep -q "feature/\*)" docs/system/workspace/scripts/worktree/wt-close && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- status: pass

## Unit
- acceptance_target: code correct
- testing_layer: unit
- required_evidence: 2 acceptance PASS

## Integration
- not_applicable_reason: bash_script_logic_change_no_runtime_dependency
- not_applicable_explanation: consistency check is defensive, unit test verifies existence

## End-to-End
- not_applicable_reason: workflow_change_needs_multi_worktree_scenario
- not_applicable_explanation: E2E requires actual dirty/sync scenarios, tested in production
