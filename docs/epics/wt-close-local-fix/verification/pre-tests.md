# Pre-Tests: wt-close local fix
- issue_id: I-20260626T142357Z-A
### acceptance-1
- acceptance_target: no 'local' outside function in wt-close
- testing_layer: unit
- test_command: grep -n 'local _dev_wt' docs/system/workspace/scripts/worktree/wt-close && echo "FAIL" || echo "PASS"
- expected_output: PASS (0 occurrences)
- actual_output: PASS — local removed
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed
### acceptance-2
- acceptance_target: bash syntax valid
- testing_layer: integration
- test_command: bash -n docs/system/workspace/scripts/worktree/wt-close && echo "OK"
- expected_output: OK
- actual_output: Syntax OK
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed
### acceptance-3
- acceptance_target: wt-close --help works
- testing_layer: end-to-end
- test_command: ./bin/wt-close --help 2>&1 | head -3
- expected_output: Usage
- actual_output: Usage text displayed
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed
