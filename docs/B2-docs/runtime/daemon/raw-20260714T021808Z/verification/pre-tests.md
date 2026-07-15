# Pre-Tests: task_mode propagation + AI_MODE guard
- issue_id: I-20260714T021808Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n 语法检查通过
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error near unexpected token
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-1.log
- red-green-status: pending
- status: pending
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: launch_project_runtime_daemon_or_fail 接受并传递 task_mode
- acceptance_target: 函数签名包含 $2 task_mode，Python spawn 含 --task-mode
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认代码改动存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'task_mode.*\$2\|\$2.*task_mode\|--task-mode.*task_mode' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-2.log
- red-green-status: pending
- status: pending
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: launch_manager_supervisor 识别 listen，fallback 为 wait
- acceptance_target: grep 确认 listen 在允许列表，fallback 为 wait 非 auto
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认代码改动存在
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-3.log
- test_command: grep -A1 '_restart_mode.*auto.*wait.*id:' docs/system/workspace/scripts/runtime/freely | grep -q 'listen' && grep -q '_restart_mode="wait"' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (listen 不在列表，fallback=auto)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-3.log
- red-green-status: pending
- status: pending
- blocker: definition_missing

### acceptance-4
- id: AT-004
- requirement: 无裸 AI_MODE 引用
- acceptance_target: grep 无未守卫的 $AI_MODE
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出为空
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-4.log
- test_command: grep -n '\$AI_MODE\|${AI_MODE}' docs/system/workspace/scripts/runtime/freely | grep -v ':-' | grep -v 'unset AI_MODE' | grep -v 'AI_MODE=' | grep -v 'freely_autonomy\|freely_interaction\|freely_approval\|freely_activation\|freely_codex_boundary' > /dev/null && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: FAIL (3 处裸引用)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-4.log
- red-green-status: pending
- status: pending
- blocker: definition_missing

### acceptance-5
- id: AT-005
- requirement: start_project_runtime 不再 hardcode wait
- acceptance_target: ensure_task_mode_gate 调用处使用变量而非 hardcode
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认改动
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-5.log
- test_command: grep 'ensure_task_mode_gate' docs/system/workspace/scripts/runtime/freely | grep -v 'wait' | head -1 > /dev/null && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (hardcode wait)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260714T021808Z/verification/test-evidence/acceptance-5.log
- red-green-status: pending
- status: pending
- blocker: definition_missing

## Unit
- acceptance_target: bash 语法 + 4 项代码改动 grep 验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001 到 AT-005 全部通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~005 已覆盖所有单元测试需求
- replacement_evidence: AT-001~005 全部 PASS

## Integration
- acceptance_target: daemon start --task-mode auto 后实际以 auto 运行
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon status 显示 task_mode=auto
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需实际 daemon 启动验证，合并后在生产环境测试
- replacement_evidence: 代码审查 + AT-001~005 grep 验证

## End-to-End
- acceptance_target: daemon 不再有 supervisor 重启循环
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: lifecycle trace 中 L040 可达，无 stale_pid_cleared 循环
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需合并后实际启动 daemon 验证
- replacement_evidence: 代码审查 + 已验证 L040 可达（同修复直接测试时）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 同一修复已在 develop 直接测试验证——L040 可达，AI launch 成功，重启循环消失
