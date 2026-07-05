# Pre-Tests: adapter/ACP dispatch 注册表驱动化

## Acceptance Items

### A1: tool_supported_adapters 注册表驱动
- acceptance_target: 已注册工具返回 adapters.supported，Cline 返回 direct+acp
- testing_layer: unit
- test_command: grep -c "_tool_registry_get.*adapters.supported\|_tool_registry_get.*adapters.default" docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: ">=1"
- actual_output:
- evidence_file:

### A2: launch_kinds 注册表驱动
- acceptance_target: 从 registry 读取而非硬编码 case
- testing_layer: unit
- test_command: grep -c "_tool_registry_get.*launch_kinds" docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: ">=1"
- actual_output:
- evidence_file:

### A3: ACP dispatch 通用路径
- acceptance_target: *) 分支不直接报错，走通用路径
- testing_layer: unit
- test_command: grep -c "unsupported ACP launcher" docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: "0"
- actual_output:
- evidence_file:

### A4: claude/codex/opencode 回归
- acceptance_target: 三工具 adapter + launch_kind 查询结果不变
- testing_layer: integration
- test_command: for t in claude codex opencode; do echo "$t: $(python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml "$t" adapters.supported)"; done
- expected_output: "claude: direct acp\ncodex: direct acp\nopencode: direct acp"
- actual_output:
- evidence_file:

### A5: _resolve_tool_family alias 扫描
- acceptance_target: registry aliases 中的二进制名正确解析
- testing_layer: unit
- test_command: grep -c "aliases\|_tool_registry.*alias" docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: ">=2"
- actual_output:
- evidence_file:

### A6: monitor-ai-acp.sh 无硬编码 fallback
- acceptance_target: 不包含 case claude/codex/opencode 硬编码
- testing_layer: unit
- test_command: grep -c "case.*claude.*codex.*opencode\|claude).*permissionMode" docs/system/workspace/scripts/runtime/monitor-ai-acp.sh
- expected_output: "0"
- actual_output:
- evidence_file:
