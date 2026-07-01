# Pre-Tests: get_config → bash indirect expansion
- issue_id: I-20260701T013527Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: daemon 启动不再报 `get_config: command not found` 错误
- acceptance_target: daemon-launch.log 中无 get_config 相关错误
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: daemon 启动日志中无 `get_config` 字符串
- evidence_level: real_env
- artifact_ref: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-1.log
- test_command: grep -c "get_config" .freely/logs/daemon-launch.log; test $? -eq 1
- expected_output: exit code 1 (no match found)
- expected_RED_output: grep 匹配到至少 1 处 `get_config` error
- actual_RED_output: "freely: line 14052: get_config: command not found" — 确认 bug 可复现，daemon-launch.log 中多处报错
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-1.log
- red-green-status: red
- status: failed
- blocker: (失败时填写)
- not_applicable_reason: (not_applicable 时填写)
- not_applicable_explanation: (not_applicable 时填写)
- replacement_evidence: (not_applicable 时填写)
- red_how: fix: grep 确认 L14052 调用未定义的 get_config，daemon-launch.log 中确认为 "get_config: command not found" 错误。get_config 函数在整个脚本中无定义。

### acceptance-2
- id: AT-002
- requirement: daemon 能正常启动后 task-mode 为 auto
- acceptance_target: daemon status 显示 running + task_mode=auto
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: daemon status 输出
- evidence_level: real_env
- artifact_ref: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-2.log
- test_command: ./bin/freely daemon start --project $(pwd) --task-mode auto --force --reason "test-red" 2>&1; ./bin/freely task-mode get --project $(pwd)
- expected_output: task_mode: auto
- expected_RED_output: daemon-launch.log 含 get_config 错误（当前修复前状态）
- actual_RED_output: 修复前 daemon-launch.log 记录 "get_config: command not found" — RED 确认
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-2.log
- red-green-status: red
- status: failed
- blocker: (失败时填写)
- red_how: fix: 修复前启动 daemon，daemon-launch.log 出现 get_config 错误，确认 bug 影响 daemon 启动

## Unit
- acceptance_target: 确认 get_config 在脚本中无定义、无其他调用点
- testing_layer: unit
- target_environment: fix/raw-20260701T013527Z-get-config-undefined
- required_evidence: grep 输出确认仅 1 处调用且无定义
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 该修复是纯 bash 语法修复，grep 验证已覆盖
- replacement_evidence: grep 验证结果

## Integration
- acceptance_target: ACP bridge 能正常启动并与 AI tool 通信
- testing_layer: integration
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: daemon 状态显示 acp_bridge_started 事件
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: daemon 完整启动 → supervisor running → agent 可接受 prompt
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined → develop merge chain
- required_evidence: daemon launch 成功，无 get_config 错误
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: fail
- real_environment_reason: RED 阶段：修复前 daemon 启动出现 get_config 错误
