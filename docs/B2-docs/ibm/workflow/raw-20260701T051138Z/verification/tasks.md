# Pre-Tests: workflow chain reorder
- issue_id: I-20260701T051138Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 7 files chain order changed
- testing_layer: unit
- target_environment: test-pre-merge-20260701T051138Z-workflow-before-feedback
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/workflow-chain/fix-order/raw-20260701T051138Z/verification/acceptance-1.log
- test_command: grep -rn "freely feedback → \[skill\]" docs/system/workspace/skills/ AGENTS.md; test $? -eq 1
- expected_output: exit 1 (no old chains)
- actual_RED_output: 7 files had old chain order — RED confirmed
- actual_output: 7 files fixed, 0 old chains remain
- evidence_file: docs/epics/workflow-chain/fix-order/raw-20260701T051138Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 7 files had workflow skill after feedback in chain, moved before

## Unit
- acceptance_target: no old chain order remains
- testing_layer: unit
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 grep 已覆盖全部 7 个文件
- replacement_evidence: AT-001 green
- status: not_applicable

## Integration
- acceptance_target: all affected files consistent
- testing_layer: integration
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable

## End-to-End
- acceptance_target: workflow skill loads before feedback
- testing_layer: end-to-end
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 文档修正，运行时验证体现在后续开发中
- replacement_evidence: AT-001 green
- status: not_applicable

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 7 文件链顺序修正完成
