# Pre-Tests
- issue_id: I-20260703T114618Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: daemon AI cycle writes __manager__ record to agent_working
- acceptance_target: agent_working.get_all has __manager__ row with manager_01
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1
- case_design: start daemon, wait for AI cycle, verify agent_working table
- target_environment: test-pre-merge
- required_evidence: rows=1, raw_key=__manager__, manager_id=manager_01
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T114618Z/verification/test-evidence/acceptance-1.log
- test_command: verify agent_working.get_all returns __manager__ row
- expected_output: __manager__ row with manager_01
- expected_RED_output: 0 rows
- actual_RED_output: 0 rows (gap: only watchdog_sse writes, not daemon startup)
- actual_output: __manager__ row confirmed, manager_id=manager_01
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T114618Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 agent_working 表为空，__manager__ 只在 _handle_needs_manager 触发时才创建

## Unit
- acceptance_target: agent_working write at session anchor
- testing_layer: unit
- target_environment: test-pre-merge
- required_evidence: record written on first AI cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖端到端
- replacement_evidence: AT-001 test-evidence/acceptance-1.log

## Integration
- acceptance_target: agent_working write at session anchor
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: record written on first AI cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖端到端
- replacement_evidence: AT-001 test-evidence/acceptance-1.log

## End-to-End
- acceptance_target: agent_working write at session anchor
- testing_layer: end-to-end
- target_environment: test-pre-merge
- required_evidence: record written on first AI cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖端到端
- replacement_evidence: AT-001 test-evidence/acceptance-1.log

## Real-Environment
- real_environment_status: pass
- real_environment_reason: test-pre-merge daemon 验证通过
