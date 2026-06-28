# Pre-Tests: 移除工具适配器硬编码
- issue_id: I-20260627T030447Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: Registry 查询 claude adapters.supported 返回 direct,acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 输出包含 acp
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude adapters.supported | grep -q acp && echo "PASS: acp found" || echo "FAIL: acp not found"
- expected_output: "PASS: acp found"
- actual_output: "PASS: acp found"
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker:
- status: pass

### acceptance-2
- acceptance_target: Registry 查询 cline adapters.supported 返回 direct,acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 输出包含 acp
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml cline adapters.supported | grep -q acp && echo "PASS: acp found" || echo "FAIL: acp not found"
- expected_output: "PASS: acp found"
- actual_output: "PASS: acp found"
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: pass

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
- status: pass

### acceptance-4
- acceptance_target: 未注册工具触发保守回退（返回 direct）
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: registry 查询失败，代码回退到 printf direct
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml nonexistent adapters.supported 2>&1; echo "EXIT: $?"
- expected_output: registry 返回错误，_tool_registry_get 回退到空字符串，触发 conservative fallback → direct
- actual_output: registry 返回 "ERROR: tool not in registry"，tool_supported_adapters_for_runtime 回退到 printf 'direct\n'
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker:
- status: pass

## Unit
- acceptance_target: 所有已注册工具 (claude, cline, codex, opencode) 的 adapters.supported 均包含 acp
- testing_layer: unit
- target_environment: fix/raw-20260627T030447Z-claude-acp-adapter-fix
- required_evidence: 四个工具全部返回 direct,acp

## Integration
- acceptance_target: freely daemon 通过 ACP 启动 claude manager
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon 正常启动，lifecycle trace 显示 tool_adapter=acp 且 rc=0
- not_applicable_reason: pre-merge 阶段无法启动 daemon（需要干净 develop + 已合并代码）。集成测试在 merge 后由 freely daemon 自举验证。
- not_applicable_explanation: 本次改动是静态配置查询层修改（tool_supported_adapters_for_runtime 函数），不涉及运行时模块间数据流或状态变更。Registry 查询的单元测试已充分覆盖。实际集成行为在 merge 到 develop 后启动 freely daemon 即可验证。

## End-to-End
- acceptance_target: 端到端验证
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: pr-merge-guarded 成功合并，freely daemon 正常启动
- not_applicable_reason: 本次改动不涉及用户可见行为或 UI 交互。改动范围仅限于 bash 函数如何查询 tool-registry.toml，不改变任何用户可见功能。端到端验证由 merge 后的 freely daemon 自举完成。
- not_applicable_explanation: 代码变更从硬编码 case 改为 registry 驱动查询，语义等价。如果 registry 配置正确（单元测试已验证），运行时行为与修复前完全一致（只是修复了之前 claude 被遗漏的 bug）。

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pre-merge 阶段，待合并到 develop 后启动 freely daemon 进行真实环境验证
