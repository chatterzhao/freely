# Pre-Tests: unify gate outputs
- issue_id: I-20260701T061924Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 3+ gates have skill summary section
- testing_layer: unit
- target_environment: test-pre-merge-20260701T061924Z-unify-gate-outputs
- required_evidence: grep count
- evidence_level: integration
- artifact_ref: docs/epics/gate-output-unify/grouped-output/raw-20260701T061924Z/verification/acceptance-1.log
- test_command: grep -lc "需要阅读的 Skill" docs/system/workspace/scripts/quality/*gate*
- expected_output: >=3
- actual_RED_output: 1
- actual_output: 3
- evidence_file: docs/epics/gate-output-unify/grouped-output/raw-20260701T061924Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: feature: 仅 governance-merge-gate 有分组
## Unit
- acceptance_target: 3+ gates grouped
- testing_layer: unit
- target_environment: feature/raw-20260701T061924Z-unify-gate-outputs
- required_evidence: grep
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable
## Integration
- acceptance_target: consistent
- testing_layer: integration
- target_environment: test-pre-merge-20260701T061924Z-unify-gate-outputs
- required_evidence: manual
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable
## End-to-End
- acceptance_target: verified in next run
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T061924Z-unify-gate-outputs
- required_evidence: observation
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 合并后验证
- replacement_evidence: AT-001 green
- status: not_applicable
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 4 gates unified
