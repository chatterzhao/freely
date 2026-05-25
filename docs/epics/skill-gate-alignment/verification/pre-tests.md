# Pre-Tests: skill gate alignment
- issue_id: I-20260508T011858Z-A

## Unit
- acceptance target: skill 示例格式正确，无冗余
- testing layer: unit
- target environment: feature worktree
- required evidence: diff review passed
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: 文档修改通过 diff 审查验证
- replacement_evidence: git diff develop..HEAD 审查通过

## Integration
- acceptance target: merge chain feature→test-pre-merge 通过
- testing layer: integration
- target environment: test-pre-merge worktree
- required evidence: pr-merge-guarded 输出无错误
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯文档修改，无运行时集成面
- replacement_evidence: pr-merge-guarded 成功输出

## End-to-End
- acceptance target: feature→test-pre-merge→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 文档修改，端到端验证即合并链本身
- replacement_evidence: pr-merge-guarded merge commits

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 部署后 skills 可正常加载，deploy-skills 验证通过

## Acceptance Items
### AT-001 skill examples complete
- id: skill-examples
- requirement: 三个 skill 示例覆盖全部必需字段，无冗余叙述
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/skill-gate-alignment/code-reviews/closeout-review.md
