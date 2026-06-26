# Pre-Tests: agent-table slot pinning
- issue_id: I-20260626T171144Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: _init_agent_table_slot_pin function exists and is called at startup
- testing_layer: unit
- test_command: grep "_init_agent_table_slot_pin" docs/system/workspace/scripts/runtime/freely | wc -l
- expected_output: >=2 (definition + call site)
- actual_output: 2
- status: pass
### acceptance-2
- acceptance_target: pr-merge-guarded --dry-run gate passes
- testing_layer: integration
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260626T171144Z-agent-table-slot-pin --dry-run
- expected_output: --dry-run complete, exit 0
- actual_output: --dry-run complete, exit 0
- status: pass
## Unit
- acceptance_target: function exists and is called
- testing_layer: unit
- required_evidence: acceptance-1 pass
## Integration
- acceptance_target: dry-run gate passes
- testing_layer: integration
- required_evidence: acceptance-2 pass
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260626T171144Z-agent-table-slot-pin --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
- status: pass
## End-to-End
- acceptance_target: daemon start correctly pins agent-table slot
- testing_layer: end-to-end
- not_applicable_reason: E2E requires merge + daemon restart to validate slot is correctly pinned
- not_applicable_explanation: slot pinning takes effect at daemon start, only testable post-merge
## Real-Environment
- real_environment_status: not_tested
