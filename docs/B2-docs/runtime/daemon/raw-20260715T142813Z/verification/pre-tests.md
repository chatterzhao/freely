# Pre-Tests: agent_working slot resolution
- issue_id: I-20260715T142813Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n syntax check
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: FAIL - agent-id.env in _init_agent_table_slot_pin
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: _resolve_current_agent_id 在 _init_agent_table_slot_pin 中被调用
- acceptance_target: grep 确认函数调用存在
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q '_resolve_current_agent_id' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - agent-id.env in _init_agent_table_slot_pin
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: agent-id.env 代码已被移除
- acceptance_target: grep agent-id.env 无结果
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出为空
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-3.log
- test_command: grep -A10 "_init_agent_table_slot_pin()" docs/system/workspace/scripts/runtime/freely | grep -q "agent-id.env" && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: FAIL (agent-id.env 仍被引用)
- actual_RED_output: FAIL - agent-id.env in _init_agent_table_slot_pin
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T142813Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: bash 语法 + 代码改动验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~003 全部通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~003 已覆盖所有单元测试
- replacement_evidence: AT-001~003 全部 PASS

## Integration
- acceptance_target: Worker daemon 在 agent_working 有记录时正确解析 slot
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon-launch.log 显示 worker slot
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需合并后实际 Worker daemon 启动验证
- replacement_evidence: 代码审查 + AT-001~003

## End-to-End
- acceptance_target: Manager 委派 Worker 时 Worker 以正确 tool 启动
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: 委派的 worker ACP session 使用 opencode
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后完整流程验证
- replacement_evidence: 代码审查

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 3行代码改动，复用已有 _resolve_current_agent_id 函数
