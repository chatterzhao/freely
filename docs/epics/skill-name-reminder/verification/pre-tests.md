# Pre-Tests
- issue_id: I-20260508T154706Z-A
## Unit
- acceptance target: --skill fix-execution accepted
- testing layer: unit
- target environment: feature worktree
- required evidence: wt-create succeeds
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Shell script verified by direct execution
- replacement_evidence: wt-create 成功输出
## Integration
- acceptance target: reminder message printed
- testing layer: integration
- target environment: develop merge chain
- required evidence: output contains "下一步"
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 验证通过实际执行
- replacement_evidence: 提醒消息正确显示
## End-to-End
- acceptance target: merge to develop
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 合并即验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: e2e 验证通过
## Acceptance Items
### AT-001 skill name
- id: skill-name
- requirement: --skill fix-execution 成功
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/skill-name-reminder/code-reviews/review.md
