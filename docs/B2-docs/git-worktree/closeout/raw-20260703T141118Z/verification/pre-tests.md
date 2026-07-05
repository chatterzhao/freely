# Pre-Tests
- issue_id: I-20260703T141118Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bridge 不再每 cycle 重启
- acceptance_target: daemon log has 0 "binary changed" or "tool changed"
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1
- case_design: start daemon, check log for bridge restart messages after 2+ cycles
- target_environment: test-pre-merge
- required_evidence: 0 bridge restarts
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T141118Z/verification/test-evidence/acceptance-1.log
- test_command: grep "binary changed\|tool changed" .freely/logs/daemon-launch.log | wc -l
- expected_output: 0
- expected_RED_output: 3 per 3 cycles
- actual_RED_output: 3+ bridge restarts every cycle (before fix)
- actual_output: 0 bridge restarts after 2 cycles
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T141118Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: before fix: bridge restarted every cycle due to full path vs short name mismatch

### acceptance-2
- id: AT-002
- requirement: tool registry 误报消失
- acceptance_target: 0 "未在 tool-registry" errors
- testing_layer: integration
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A3
- target_environment: test-pre-merge
- required_evidence: 0 tool registry errors
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T141118Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "未在 tool-registry" .freely/logs/daemon-launch.log
- expected_output: 0
- expected_RED_output: 17 occurrences
- actual_RED_output: 17 occurrences (before fix)
- actual_output: 0
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T141118Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: before fix: shell for-loop matching failed despite opencode being in registry list

## Unit
- acceptance_target: bridge not restarting every cycle
- testing_layer: unit
- target_environment: test-pre-merge
- required_evidence: 0 bridge restarts + 0 tool registry errors
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 cover end-to-end
- replacement_evidence: AT-001/002 acceptance logs

## Integration
- acceptance_target: bridge not restarting every cycle
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: 0 bridge restarts + 0 tool registry errors
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 cover end-to-end
- replacement_evidence: AT-001/002 acceptance logs

## End-to-End
- acceptance_target: bridge not restarting every cycle
- testing_layer: end-to-end
- target_environment: test-pre-merge
- required_evidence: 0 bridge restarts + 0 tool registry errors
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 cover end-to-end
- replacement_evidence: AT-001/002 acceptance logs

## Real-Environment
- real_environment_status: pass
- real_environment_reason: test-pre-merge daemon verified
