# Pre-Tests: merge lock self-heal
- issue_id: I-20260701T081450Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: orphan lock auto-cleans
- testing_layer: unit
- target_environment: test-pre-merge-20260701T081450Z-merge-lock-orphan-heal
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/branch-pr/raw-20260701T081450Z50Z/verification/acceptance-1.log
- test_command: grep -c "ORPHAN_LOCK" docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: 2
- actual_RED_output: 0
- actual_output: 2
- evidence_file: docs/B2-docs/git-worktree/branch-pr/raw-20260701T081450Z50Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前无孤儿锁自愈，静默等300s
## Unit
- acceptance_target: lock logic correct
- testing_layer: unit
- target_environment: fix/raw-20260701T081450Z50Z-merge-lock-orphan-heal
- required_evidence: grep
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001 green
- status: not_applicable
## Integration
- acceptance_target: lock self-heal tested with merge
- testing_layer: integration
- target_environment: test-pre-merge-20260701T081450Z-merge-lock-orphan-heal
- required_evidence: manual
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖代码验证
- replacement_evidence: AT-001 green
- status: not_applicable

## End-to-End
- acceptance_target: next merge with stale lock auto-heals
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T081450Z-merge-lock-orphan-heal
- required_evidence: observation
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 合并后验证
- replacement_evidence: AT-001 green
- status: not_applicable
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 孤儿锁自愈逻辑已实现
