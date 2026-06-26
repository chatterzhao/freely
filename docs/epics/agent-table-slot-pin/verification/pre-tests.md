# Pre-Tests: agent-table slot pinning
- issue_id: I-20260626T171144Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: _init_agent_table_slot_pin 在启动时调用
- testing_layer: unit
- test_command: grep "_init_agent_table_slot_pin" docs/system/workspace/scripts/runtime/freely
- expected_output: function defined and called
- actual_output: function at line 4555, call at line 21357
- status: pass
## Unit
- acceptance_target: 代码验证
- testing_layer: unit
- required_evidence: acceptance-1 pass
## Integration
- acceptance_target: pr-merge-guarded --dry-run
- testing_layer: integration
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260626T171144Z-agent-table-slot-pin --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
- status: pass
## End-to-End
- acceptance_target: daemon start 后 slot 正确 pin 到 agent-table 值
- testing_layer: end-to-end
- not_applicable_reason: 需 merge 后重启 daemon 验证
## Real-Environment
- real_environment_status: not_tested
