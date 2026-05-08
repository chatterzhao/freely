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
## End-to-End
- acceptance target: merge chain passes
- testing layer: end_to_end
- target environment: develop-bound merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 部署后 skills 可正常加载
## Acceptance Items
### AT-001 skill examples
- id: skill-examples
- requirement: 三个 skill 示例覆盖全部必需字段
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/skills/doc-B1_IBM-execution/SKILL.md
