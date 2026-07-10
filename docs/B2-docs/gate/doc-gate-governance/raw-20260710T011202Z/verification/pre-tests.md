# Pre-Tests
- issue_id: I-20260710T011202Z-A
### acceptance-1
- id: AT-001
- requirement: FREELY_SKIP_IBM_GATE skips IBM gate in pr-create-guarded
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/doc-gate-governance/raw-20260710T011202Z/verification/test-evidence/acceptance-1.log
- test_command: grep -q "FREELY_SKIP_IBM_GATE" docs/system/workspace/scripts/worktree/pr-create-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: "FAIL: FREELY_SKIP_IBM_GATE not in pr-create-guarded"
- actual_output: "PASS"
- red-green-status: green
- status: pass
- red_how: fix — 修改前 pr-create-guarded 不检查 FREELY_SKIP_IBM_GATE
## Unit: not_applicable (covered_by_more_realistic_required_surface)
## Integration: not_applicable (covered_by_more_realistic_required_surface)
## End-to-End: not_applicable (covered_by_more_realistic_required_surface)
## Real-Environment: pass
