# Pre-Tests: 移除工具适配器硬编码
- issue_id: I-20260627T030447Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: Registry 查询 claude adapters.supported 返回 direct,acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 输出包含 acp
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude adapters.supported | grep -q acp && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker:
- status: passed

### acceptance-2
- acceptance_target: Registry 查询 cline adapters.supported 返回 direct,acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 输出包含 acp
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml cline adapters.supported | grep -q acp && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: passed

### acceptance-3
- acceptance_target: Registry 查询 claude adapters.default 返回 acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 输出为 acp
- test_command: result=$(python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude adapters.default) && [[ "$result" == "acp" ]] && echo "PASS: $result" || echo "FAIL: $result"
- expected_output: "PASS: acp"
- actual_output: "PASS: acp"
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker:
- status: passed

### acceptance-4
- acceptance_target: 未注册工具返回空（保守回退到 direct）
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 查询不存在工具返回空字符串
- test_command: result=$(python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml nonexistent adapters.supported 2>&1) && [[ -z "$result" ]] && echo "PASS: empty" || echo "FAIL: $result"
- expected_output: "PASS: empty"
- actual_output: "PASS: empty"
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker:
- status: passed

## Unit
- acceptance_target: 所有已注册工具 (claude, cline, codex, opencode) 的 adapters.supported 均包含 acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 四个工具全部返回 direct,acp

## Integration
- acceptance_target: freely daemon 可通过 ACP 启动 claude manager
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon 正常启动，lifecycle trace 显示 tool_adapter=acp 且 rc=0

## End-to-End
- acceptance_target: 端到端验证
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: pr-merge-guarded 成功合并
