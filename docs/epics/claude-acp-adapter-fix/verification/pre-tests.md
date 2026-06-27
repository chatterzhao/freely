# Pre-Tests: 移除工具适配器硬编码
- issue_id: I-20260627T030447Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: `tool_supported_adapters_for_runtime` 对 claude 返回 acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 函数输出包含 acp
- test_command: source docs/system/workspace/scripts/runtime/freely && tool_supported_adapters_for_runtime "claude" | grep -Fxq "acp" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output:
- evidence_file:
- blocker:
- status: pending

### acceptance-2
- acceptance_target: `tool_supported_adapters` (tool-launchers.sh) 对 claude 返回 acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 函数输出包含 acp
- test_command: source docs/system/workspace/scripts/runtime/tool-launchers.sh && tool_supported_adapters "claude" | grep -Fxq "acp" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output:
- evidence_file:
- blocker:
- status: pending

### acceptance-3
- acceptance_target: `tool_default_adapter` (tool-launchers.sh) 对 claude 返回 acp（从 registry 读）
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 返回 acp
- test_command: source docs/system/workspace/scripts/runtime/tool-launchers.sh && result=$(tool_default_adapter "claude") && [[ "$result" == "acp" ]] && echo "PASS: $result" || echo "FAIL: $result"
- expected_output: "PASS: acp"
- actual_output:
- evidence_file:
- blocker:
- status: pending

### acceptance-4
- acceptance_target: 未注册工具返回 direct only（保守回退）
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 对不存在的工具返回 direct
- test_command: source docs/system/workspace/scripts/runtime/tool-launchers.sh && result=$(tool_supported_adapters "nonexistent-tool" | tr '\n' ',' | sed 's/,$//') && [[ "$result" == "direct" ]] && echo "PASS: $result" || echo "FAIL: $result"
- expected_output: "PASS: direct"
- actual_output:
- evidence_file:
- blocker:
- status: pending

## Unit
- acceptance_target: 两个 `tool_default_adapter` 函数一致性
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 对 claude 返回相同值 acp
- not_applicable_reason:
- not_applicable_explanation:
- replacement_evidence:

## Integration
- acceptance_target: freely daemon 可通过 ACP 启动 claude manager
- testing_layer: integration
- target_environment: test-pre-merge-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: daemon 正常启动，lifecycle trace 显示 ai_launch_begin tool_adapter=acp 且 rc=0
