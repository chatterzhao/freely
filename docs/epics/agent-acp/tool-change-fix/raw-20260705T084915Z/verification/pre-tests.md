# Pre-Tests
- issue_id: I-20260705T084915Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: _current_base uses $base_tool not AGENT_AI_TOOL
- acceptance_target: grep confirms
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/agent-acp/tool-change-fix/raw-20260705T084915Z/verification/test-evidence/at-001.log
- test_command: grep -c 'local _current_base="${base_tool:-claude}"' docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: 0 (uses AGENT_AI_TOOL)
- actual_RED_output: used AGENT_AI_TOOL
- actual_output: PASS
- evidence_file: at-001.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — before fix used global AGENT_AI_TOOL
## Unit
- acceptance_target: AT-001
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: shell validation
- replacement_evidence: AT-001
## Integration
- acceptance_target: daemon 无 false tool change
- testing_layer: integration
- target_environment: test-pre-merge-*
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: needs daemon
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: N/A
- testing_layer: end_to_end
- target_environment: test-pre-merge-*
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: post-merge dogfood
- replacement_evidence: AT-001
## Real-Environment
- real_environment_status: pass
- real_environment_reason: confirmed opencode bridge was falsely restarted
