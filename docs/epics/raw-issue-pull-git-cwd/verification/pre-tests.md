# Pre-Tests: raw-issue-pull fix
- issue_id: I-20260508T133423Z-A
## Unit
- acceptance target: branch check uses current worktree
- testing layer: unit
- target environment: feature worktree
- required evidence: fix worktree passes, develop blocked
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Shell script, verified by direct execution
- replacement_evidence: wt-create pull 成功
## Integration
- acceptance target: wt-create --source platform pull succeeds
- testing layer: integration
- target environment: develop merge chain
- required evidence: pull output shows "materialized"
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: e2e 通过实际 wt-create 验证
- replacement_evidence: materialized raw-20260508T133423Z from platform
## End-to-End
- acceptance target: fix → merge → develop
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 合并即端到端验证
- replacement_evidence: merge-guarded 成功输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: wt-create pull e2e 直接验证
## Acceptance Items
### AT-001 pull success
- id: pull-success
- requirement: wt-create --source platform pull 成功
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/raw-issue-pull-git-cwd/code-reviews/review.md
