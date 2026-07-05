# Pre-Tests
- issue_id: I-20260508T232413Z-A
## Unit
- acceptance target: error output includes IBM guidance
- testing layer: unit
- target environment: feature worktree
- required evidence: output text matches expected format
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Shell output, verified by direct inspection
- replacement_evidence: pr-merge-guarded 输出验证
## Integration
- acceptance target: merge blocked with clear IBM guidance
- testing layer: integration
- target environment: develop merge chain
- required evidence: merge failure output includes self-diagnosis
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 集成通过实际 merge 验证
- replacement_evidence: pr-merge-guarded 输出
## End-to-End
- acceptance target: fix → merge → develop
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 合并即验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 输出格式直接确认
## Acceptance Items
### AT-001 ibm guidance
- id: ibm-guidance
- requirement: merge error output guides AI through IBM self-diagnosis
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/merge-error-ibm-guide/code-reviews/review.md
