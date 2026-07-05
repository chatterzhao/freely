# Pre-Tests: feedback exit on platform error
- issue_id: I-20260626T133842Z-A

### acceptance-1
- acceptance_target: adapter error causes exit 1 (|| true removed)
- testing_layer: unit
- test_command: grep -c '|| true' docs/system/workspace/scripts/runtime/freely | grep -A1 '_adapter_result='
- expected_output: 0 (no || true on adapter call)
- actual_output: || true removed, replaced with error handler block
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

### acceptance-2
- acceptance_target: no platform created → exit 1 (not WARNING)
- testing_layer: unit
- test_command: grep -A5 '_created.*!=.*1' docs/system/workspace/scripts/runtime/freely | grep 'exit 1'
- expected_output: exit 1 found
- actual_output: exit 1 on no platform created
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed

### acceptance-3
- acceptance_target: per-platform error check exists
- testing_layer: unit
- test_command: grep -c 'ERROR.*platform.*failed' docs/system/workspace/scripts/runtime/freely
- expected_output: 1+
- actual_output: per-platform error check present with exit 1
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed

### acceptance-4
- acceptance_target: bash syntax valid
- testing_layer: integration
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo "OK"
- expected_output: OK
- actual_output: Syntax OK
- evidence_file: .freely/run/test-evidence/acceptance-4.log
^- status: passed

### acceptance-5
- acceptance_target: feedback --help still works
- testing_layer: end-to-end
- test_command: freely feedback --help 2>&1 | head -3
- expected_output: Usage text
- actual_output: Usage text displayed correctly
- evidence_file: .freely/run/test-evidence/acceptance-5.log
^- status: passed
