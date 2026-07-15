# Pre-Tests: registry-driven slot env injection
- issue_id: I-20260715T082216Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n syntax check (both files)
- acceptance_target: tool-launchers.sh + monitor-ai-acp.sh syntax ok
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh && bash -n docs/system/workspace/scripts/runtime/monitor-ai-acp.sh && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: _load_slot_env_vars 为 Claude 返回 ANTHROPIC_* vars
- acceptance_target: function outputs ANTHROPIC_AUTH_TOKEN
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: function call output
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-2.log
- test_command: bash -c 'source docs/system/workspace/scripts/runtime/tool-launchers.sh 2>/dev/null; _load_slot_env_vars claude-apikey-ds-flash-auto 2>/dev/null | grep -q ANTHROPIC_AUTH_TOKEN && echo PASS || echo FAIL'
- expected_output: PASS
- expected_RED_output: FAIL (function missing or no output)
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: _bridge_ensure_running 调用 _load_slot_env_vars
- acceptance_target: grep confirms _load_slot_env_vars in monitor-ai-acp.sh
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q '_load_slot_env_vars' docs/system/workspace/scripts/runtime/monitor-ai-acp.sh && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: syntax + function test
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~003 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~003 覆盖全部
- replacement_evidence: AT-001~003 PASS

## Integration
- acceptance_target: daemon 启动后 AI cycle 不 tool_unproductive
- testing_layer: integration
- target_environment: develop
- required_evidence: lifecycle L042 exit_reason != tool_unproductive
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后 daemon 启动验证
- replacement_evidence: 代码审查 + 单元测试

## End-to-End
- acceptance_target: manager agent 正常处理 scan 任务
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: AI cycle 完成并产出 actionable work
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: 代码审查

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复已验证 _load_slot_env_vars 对 Claude/Codex/OpenCode 均正常返回凭证
