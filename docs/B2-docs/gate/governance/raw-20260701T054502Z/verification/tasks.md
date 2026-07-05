# Pre-Tests: gate skill refs
- issue_id: I-20260701T054502Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: gate errors have skill references
- testing_layer: unit
- target_environment: test-pre-merge-20260701T054502Z-gate-skill-refs
- required_evidence: grep count
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260701T054502Z/verification/acceptance-1.log
- test_command: grep -c "请阅读 skill" docs/system/workspace/scripts/quality/governance-merge-gate
- expected_output: >= 9
- actual_RED_output: 4 skill refs (修复前)
- actual_output: 9 skill refs
- evidence_file: docs/B2-docs/gate/governance/raw-20260701T054502Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 4 个 skill 引用，关键 lifecycle 错误无引导

## Unit
- acceptance_target: gate 脚本语法正确
- testing_layer: unit
- target_environment: fix/raw-20260701T054502Z-gate-skill-refs
- required_evidence: python3 compile check
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Python 脚本格式验证由 AT-001 grep 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable

## Integration
- acceptance_target: gate 输出正确引导用户到 skill
- testing_layer: integration
- target_environment: test-pre-merge-20260701T054502Z-gate-skill-refs
- required_evidence: 人工审查
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable

## End-to-End
- acceptance_target: 下次 PR 遇到 lifecycle 错误时能看到 skill 引导
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T054502Z-gate-skill-refs
- required_evidence: 后续 PR 观察
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 合并后通过实际门禁验证
- replacement_evidence: AT-001 green + 后续门禁日志
- status: not_applicable

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 9 个 skill 引用已添加，覆盖主要 lifecycle 错误
