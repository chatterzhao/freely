# Pre-Tests
- issue_id: I-20260509T022152Z-A
## Unit
- acceptance target: non fix/feature branch rejected
- testing layer: unit
- target environment: feature worktree
- required evidence: function returns 1 for develop/test-pre-merge
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Bash logic verified by code review
- replacement_evidence: case statement checked
## Integration
- acceptance target: worker launch rejected on develop
- testing layer: integration
- target environment: develop merge chain
- required evidence: worker not launched on protected branch
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 集成需 daemon 运行验证
- replacement_evidence: pr-merge-guarded 输出
## End-to-End
- acceptance target: worker launched on fix/feature, rejected on develop/test-pre-merge
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 合并即验证
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: case 语句检查通过
## Acceptance Items
### AT-001 branch check
- id: branch-check
- requirement: worker target must be fix/* or feature/*
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/worker-launch-branch-check/code-reviews/review.md
