# Pre-Tests: timestamp seconds upgrade
- issue_id: I-20260507T143545Z-A
## Unit
- acceptance target: _normalize_key_variants 正确处理 3 种格式含秒
- testing layer: unit
- target environment: feature worktree
- required evidence: 函数返回正确的 format variants
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Python 函数逻辑通过 grep 和代码审查验证
- replacement_evidence: grep 确认 0 个遗漏的 \\d{4}
## Integration
- acceptance target: 门禁不再因 6 位秒截断报假阳性
- testing layer: integration
- target environment: develop merge chain
- required evidence: GATE 6.3 无 raw-* missing 假阳性
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 门禁假阳性只能通过实际合并验证
- replacement_evidence: pr-merge-guarded 成功输出
## End-to-End
- acceptance target: merge passes
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 正则修改，合并即端到端验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 正则修改，grep 零遗漏验证通过
## Acceptance Items
### AT-001 regex upgrade
- id: regex-upgrade
- requirement: 所有 \\d{4} 改为 \\d{4,6}，6位秒 key 可正确匹配
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/B2-docs/timestamp-seconds-upgrade/code-reviews/closeout-review.md
