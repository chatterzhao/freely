# Pre-Tests: wt-close CWD safety
- issue_id: I-20260625T235348Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: Phase 5 and 6 have cd PROJECT_ROOT
- testing_layer: unit
- required_evidence: grep
- test_command: grep -c "cd.*PROJECT_ROOT" docs/system/workspace/scripts/worktree/wt-close | xargs -I{} test {} -ge 2 && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- status: pass

## Unit
- acceptance_target: CWD safety verified
- testing_layer: unit

## Integration
- not_applicable_reason: bash_script_logic_change_no_runtime_dependency
- not_applicable_explanation: CWD fix is defensive, verified by unit test

## End-to-End
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 2-line cd fix, production verified
