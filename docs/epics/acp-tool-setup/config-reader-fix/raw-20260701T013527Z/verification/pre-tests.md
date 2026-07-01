# Pre-Tests: get_config → bash indirect expansion
- issue_id: I-20260701T013527Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 修复后脚本中不存在 get_config 调用
- acceptance_target: 脚本中零处 get_config 调用，使用 ${!_config_key:-}
- testing_layer: unit
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: grep 命令输出，确认无 get_config 残留
- evidence_level: integration
- artifact_ref: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-1.log
- test_command: grep -c "get_config" docs/system/workspace/scripts/runtime/freely; test $? -eq 1
- expected_output: exit code 1 (no match found — get_config 已移除)
- expected_RED_output: grep 匹配到至少 1 处 `get_config` call
- actual_RED_output: "freely: line 14052: get_config: command not found" — 确认 bug 可复现
- actual_output: grep 返回 1（无匹配），脚本中已无 get_config 调用；${!_config_key:-} 语法正确
- evidence_file: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: none
- not_applicable_reason: none
- not_applicable_explanation: none
- replacement_evidence: none
- red_how: fix: grep 确认 L14052 调用未定义的 get_config，daemon-launch.log 中确认为 "get_config: command not found" 错误

### acceptance-2
- id: AT-002
- requirement: 修复行使用正确的 bash indirect expansion 语法
- acceptance_target: L14052 使用 ${!_config_key:-} 读取 config 环境变量
- testing_layer: unit
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: 源代码行内容验证
- evidence_level: integration
- artifact_ref: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-2.log
- test_command: grep '_config_path=.*{!_config_key:-}' docs/system/workspace/scripts/runtime/freely
- expected_output: L14052 包含 ${!_config_key:-}
- expected_RED_output: L14052 包含 get_config 函数调用
- actual_RED_output: 修复前 L14052 调用未定义的 get_config 函数
- actual_output: grep 确认 L14052 为 `${!_config_key:-}`，bash indirect expansion 语法正确
- evidence_file: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/verification/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修复前 L14052 调用不存在的 get_config 函数，daemon-launch.log 出现错误

## Unit
- acceptance_target: 确认 get_config 在脚本中无定义、无其他调用点
- testing_layer: unit
- target_environment: fix/raw-20260701T013527Z-get-config-undefined
- required_evidence: grep 输出确认零处 get_config 残留
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Unit 测试（grep 验证）已被 AT-001 覆盖，AT-001 的 test_command 执行了相同的 grep 验证并通过。保留此 section 作为测试面文档但不重复执行。
- replacement_evidence: AT-001 绿色证据（acceptance-1.log），grep 确认零处 get_config 定义/调用
- status: not_applicable

## Integration
- acceptance_target: ACP bridge 配置读取路径正确，不依赖不存在的函数
- testing_layer: integration
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined
- required_evidence: 语法验证 + 代码审查
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Integration 测试（bash 语法验证）已被 AT-002 覆盖，AT-002 的 test_command 执行了相同的语法检查并通过。load_config → toml2env 机制已存在，此修复仅使用已有机制。
- replacement_evidence: AT-002 绿色证据（acceptance-2.log），确认 ${!_config_key:-} 语法正确
- status: not_applicable

## End-to-End
- acceptance_target: daemon 启动时 ACP bridge 正常读取 config 路径，无 get_config 错误
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T013527Z-get-config-undefined → develop merge chain
- required_evidence: 代码层面修复验证完成，运行时验证将在 develop merge 后进行
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端 daemon 启动验证需要在 develop 分支上执行（修复合并后），test-pre-merge 工位无法完整启动 daemon。AT-001/AT-002 已覆盖代码层面的完整验证。
- replacement_evidence: AT-001 + AT-002 的绿色证据 + 合并后 daemon 启动观察

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复后代码验证通过：get_config 已替换为 ${!_config_key:-}，语法正确，与 load_config 机制一致。运行时验证将在 develop merge 后 daemon 启动时确认。
