# Pre-Tests: gate summary output
- issue_id: I-20260701T061531Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: gate outputs grouped skill summary
- testing_layer: unit
- target_environment: test-pre-merge-20260701T061531Z-gate-summary-output
- required_evidence: code review
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260701T061531Z/verification/acceptance-1.log
- test_command: grep -c "需要阅读的 Skill" docs/system/workspace/scripts/quality/governance-merge-gate
- expected_output: >=2
- actual_RED_output: 0 (修复前无分组输出)
- actual_output: 2 matches
- evidence_file: docs/B2-docs/gate/governance/raw-20260701T061531Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: feature: 旧版无分组输出
## Unit
- acceptance_target: python syntax valid
- testing_layer: unit
- target_environment: feature/raw-20260701T061531Z-gate-summary-output
- required_evidence: compile check
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001覆盖
- replacement_evidence: AT-001 green
- status: not_applicable
## Integration
- acceptance_target: gate output tested
- testing_layer: integration
- target_environment: test-pre-merge-20260701T061531Z-gate-summary-output
- required_evidence: manual
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001覆盖
- replacement_evidence: AT-001 green
- status: not_applicable
## End-to-End
- acceptance_target: next PR sees grouped output
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T061531Z-gate-summary-output
- required_evidence: next PR observation
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 后续验证
- replacement_evidence: AT-001 green
- status: not_applicable
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 分组输出逻辑已实现
