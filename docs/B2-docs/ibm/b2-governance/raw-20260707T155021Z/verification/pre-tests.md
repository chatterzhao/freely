# Pre-Tests: review-guidelines 行为测试强化
- issue_id: I-20260707T155021Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: b2/red/dev/green review guidelines 都包含行为测试检查
- acceptance_target: grep 确认 4 个文件都含 "行为" 或 "grep.*FAIL"
- testing_layer: unit
- target_environment: test-pre-merge-20260707T155021Z-review-guidelines-behavioral-testing
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T155021Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "行为" docs/system/workspace/review-guidelines/b2-review.md docs/system/workspace/review-guidelines/red-review.md docs/system/workspace/review-guidelines/dev-review.md docs/system/workspace/review-guidelines/green-review.md
- expected_output: 每文件 >=1
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 review-guidelines 无行为测试要求
## Unit
- acceptance_target: 纯文档修改
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯 Markdown
- replacement_evidence: AT-001 grep
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T155021Z-review-guidelines-behavioral-testing
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文档
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: pr-create-guarded 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 GREEN
