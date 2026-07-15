# Pre-Tests: adapter variable fix
- issue_id: I-20260715T115327Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: freely script syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T115327Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T115327Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
### acceptance-2
- id: AT-002
- requirement: line 22757 uses tool_adapter not AGENT_AI_TOOL_ADAPTER
- acceptance_target: grep confirms the fix
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T115327Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'tool_adapter:-acp' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T115327Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing
## Unit
- acceptance_target: syntax + grep
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~002 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 cover
- replacement_evidence: AT-001/002 PASS
## Integration
- acceptance_target: daemon launches AI via ACP
- testing_layer: integration
- target_environment: develop
- required_evidence: lifecycle shows monitor-ai-acp.sh called, session created
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review + grep
## End-to-End
- acceptance_target: manager agent produces productive work
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: AI cycle completes with session_id (not unavailable)
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: verify after merge
- replacement_evidence: code review
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 1-line fix, variable resolution verified correct
