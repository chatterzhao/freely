# Pre-Tests: skill ref cleanup
- issue_id: I-20260508T004541Z-A
## Unit
- acceptance target: lead-agent.md references updated
- testing layer: unit
- target environment: feature worktree
- required evidence: grep confirms changes
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: 文档修改，diff 审查即可
- replacement_evidence: git diff 确认只改了 lead-agent.md
## Integration
- acceptance target: runtime scripts preserved
- testing layer: integration
- target environment: feature worktree
- required evidence: start-lead-agent.sh unchanged
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: runtime 脚本不需改
- replacement_evidence: grep 确认无意外改动
## End-to-End
- acceptance target: merge passes
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 文档修改，合并即验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 文件改动通过 diff 审查
## Acceptance Items
### AT-001 skill ref update
- id: skill-ref-update
- requirement: lead-agent.md 使用 dual-mode 引用
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/skill-ref-cleanup/code-reviews/closeout-review.md
