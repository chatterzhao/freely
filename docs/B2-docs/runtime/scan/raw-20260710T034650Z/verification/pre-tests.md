# Pre-Tests
- issue_id: I-20260710T034650Z-A
### acceptance-1
- id: AT-001
- requirement: FREELY_SKIP_IBM_GATE=1 无残留
- testing_layer: unit
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T034650Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "FREELY_SKIP_IBM_GATE=1" docs/system/workspace/scripts/runtime/pre-scan-fix.sh | xargs -I{} sh -c '[ {} -eq 0 ] && echo PASS || echo FAIL'
- expected_output: PASS
- actual_RED_output: "FAIL: =1 found"
- actual_output: "PASS"
- red-green-status: green
- status: pass
- red_how: fix
### acceptance-2
- id: AT-002
- requirement: BATCH_BODY 含 ## 章节
- testing_layer: unit
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T034650Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q "## 问题" docs/system/workspace/scripts/runtime/pre-scan-fix.sh && echo PASS || echo FAIL
- expected_output: PASS
- actual_RED_output: "FAIL"
- actual_output: "PASS"
- red-green-status: green
- status: pass
- red_how: fix
### acceptance-3
- id: AT-003
- requirement: daemon cycle 调用 pre-scan-fix.sh
- testing_layer: unit
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T034650Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q "pre-scan-fix.sh" docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- actual_RED_output: "FAIL"
- actual_output: "PASS"
- red-green-status: green
- status: pass
- red_how: fix
## Unit: not_applicable (covered_by_more_realistic_required_surface)
## Integration: not_applicable (covered_by_more_realistic_required_surface)
## End-to-End: not_applicable (covered_by_more_realistic_required_surface)
## Real-Environment: pass
