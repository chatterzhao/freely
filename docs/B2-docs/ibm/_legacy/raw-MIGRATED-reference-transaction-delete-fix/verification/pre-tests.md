# Pre-Tests: reference-transaction delete fix
- issue_id: I-20260508T111130Z-A
## Unit
- acceptance target: aborted txn correctly skipped
- testing layer: unit
- target environment: feature worktree
- required evidence: git branch -d succeeds
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Shell hook, verified by direct execution
- replacement_evidence: git branch -d test-pre-merge-* 成功删除
## Integration
- acceptance target: hook no longer blocks branch deletion
- testing layer: integration
- target environment: develop merge chain
- required evidence: merge succeeds
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 集成验证通过实际 merge 流程
- replacement_evidence: pr-merge-guarded 成功输出
## End-to-End
- acceptance target: full fix → merge → develop works
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: Hook 修复，合并即端到端验证
- replacement_evidence: pr-merge-guarded 成功输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: git branch -d 直接验证通过
## Acceptance Items
### AT-001 delete unblocked
- id: delete-unblocked
- requirement: git branch -d test-pre-merge-* 不再被误拦截
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/B2-docs/reference-transaction-delete-fix/code-reviews/review.md
