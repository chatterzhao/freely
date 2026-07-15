# Pre-Tests: revert AI_MODE default wait→auto
- issue_id: I-20260715T063959Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n 语法检查通过
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: PASS (syntax baseline)
- actual_RED_output: RED confirmed — 6 :-wait, 0 :-auto
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: 所有 AI_MODE 默认值从 wait 回退到 auto
- acceptance_target: grep AI_MODE:-wait=0, AI_MODE:-auto=6
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'AI_MODE:-wait' docs/system/workspace/scripts/runtime/freely | grep -q '^0$' && test $(grep -c 'AI_MODE:-auto' docs/system/workspace/scripts/runtime/freely) -eq 6 && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (6 :-wait present, 0 :-auto)
- actual_RED_output: RED confirmed — 6 :-wait, 0 :-auto
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: log 行 AI_MODE 守卫保持为 :-none
- acceptance_target: 3 处 AI_MODE:-none 守卫不变
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-3.log
- test_command: test $(grep -c 'AI_MODE:-none' docs/system/workspace/scripts/runtime/freely) -ge 3 && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: PASS (guards already present)
- actual_RED_output: RED confirmed — 6 :-wait, 0 :-auto
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: bash 语法 + grep 验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~003 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~003 覆盖全部
- replacement_evidence: AT-001~003 PASS

## Integration
- acceptance_target: daemon 启动后 AI launch 不报 unsupported mode
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon-launch.log 无 unsupported mode 错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: 代码审查 + grep

## End-to-End
- acceptance_target: AI 不再 tool_unproductive
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: lifecycle L042 exit_reason != tool_unproductive
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后实际 daemon 启动验证
- replacement_evidence: 代码审查

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 概念混淆修正——AI_MODE≠task_mode，回退到正确的 auto 默认值
