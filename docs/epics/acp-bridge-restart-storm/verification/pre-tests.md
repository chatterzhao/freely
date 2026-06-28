# Pre-Tests
- issue_id: I-20260508T225041Z-A
## Unit
- acceptance target: prompt generation includes companion info for test-pre-merge
- testing layer: unit
- target environment: feature worktree
- required evidence: generated prompt contains companion path
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Bash logic, verified by syntax check and code review
- replacement_evidence: bash -n passed
## Integration
- acceptance target: daemon generates worker prompt with companion info
- testing layer: integration
- target environment: develop merge chain
- required evidence: worker prompt output includes companion writable worktree
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 集成验证通过实际 daemon 运行
- replacement_evidence: daemon 输出验证
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
- real_environment_reason: bash -n 语法通过
## Acceptance Items
### AT-001 companion info
- id: companion-info
- requirement: test-pre-merge worker prompt includes companion worktree
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/acp-bridge-restart-storm/code-reviews/review.md
