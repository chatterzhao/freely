# Pre-Tests: platform-adapter title key fix
- issue_id: I-20260508T121541Z-A
## Unit
- acceptance target: title with raw-{key} skips standardization
- testing layer: unit
- target environment: feature worktree
- required evidence: key unchanged after pull
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Python logic verified by e2e wt-create test
- replacement_evidence: wt-create pull 返回正确 key
## Integration
- acceptance target: wt-create pull preserves title key
- testing layer: integration
- target environment: develop merge chain
- required evidence: materialized key matches title key
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 集成验证通过 wt-create e2e
- replacement_evidence: materialized raw-20260508T121541Z41Z
## End-to-End
- acceptance target: fix → merge → develop
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 合并即端到端验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: wt-create e2e 验证通过
## Acceptance Items
### AT-001 title key preserved
- id: title-key-preserved
- requirement: pull 后 key 与标题一致
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/B2-docs/platform-adapter-title-key/code-reviews/review.md
