# Pre-Tests: reconciliation
- issue_id: I-20260625T211813Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: --reconcile detects stale entries
- testing_layer: unit
- test_command: python3 bin/agent-table-query --reconcile 2>&1 | grep -q "Stale pool" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed
## Unit
- acceptance_target: functional
## Integration
- not_applicable_reason: static_analysis_no_runtime_dependency
- not_applicable_explanation: reconciliation is a query, no side effects
## End-to-End
- not_applicable_reason: production_only
- not_applicable_explanation: tested when daemon runs
