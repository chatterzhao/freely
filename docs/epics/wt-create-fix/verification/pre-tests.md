# Pre-Tests: wt-create fix
- issue_id: I-20260508T120000Z-A
## Unit
- acceptance target: _extract_issue_key 匹配 6 位秒
- testing layer: unit
- target environment: feature worktree
- required evidence: 6-digit key not truncated
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Shell regex 通过实际工位创建验证
- replacement_evidence: wt-create 成功创建带秒 raw-key 的工位
## End-to-End
- acceptance target: merge passes
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: Bug 修复，合并即验证
- replacement_evidence: merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复后工位创建不再需要临时 hack
## Acceptance Items
### AT-001 regex + scan_lookup
- id: wt-create-fix
- requirement: 6 位秒 key 可创建工位，scan_lookup 正确匹配
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/wt-create-fix/code-reviews/review.md
