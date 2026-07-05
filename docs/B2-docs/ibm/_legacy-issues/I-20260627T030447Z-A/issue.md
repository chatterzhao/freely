- issue_id: I-20260627T030447Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T030447Z-A
- source_candidate: docs/B1-docs/raw-20260627T030447Z/candidates.md#C-20260627T030447Z-A
- source_raw: raw-20260627T030447Z
- verification_artifact_dir: docs/B2-docs/claude-acp-adapter-fix/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260627T030447Z-A/issue.md
- pre_tests_path: docs/B2-docs/claude-acp-adapter-fix/verification/pre-tests.md
- title: 移除工具适配器硬编码，改为 registry 驱动

# I-20260627T030447Z-A: 移除工具适配器硬编码，改为 registry 驱动

- source_candidate: docs/B1-docs/raw-20260627T030447Z/candidates.md#C-20260627T030447Z-A
- verification_artifact_dir: docs/B2-docs/claude-acp-adapter-fix/code-reviews
- pre_tests_path: docs/B2-docs/claude-acp-adapter-fix/verification/pre-tests.md

## 实现
- `freely`: `tool_supported_adapters_for_runtime()` — 移除硬编码 case，改为 `_tool_registry_get("adapters.supported")`
- `freely`: `tool_default_adapter_for_runtime()` — 改为 registry 驱动，fallback acp
- `freely`: 计算 `tool_adapter` 后 `export AI_TOOL_ADAPTER`
- `tool-launchers.sh`: `tool_default_adapter()` — 改为 registry 驱动，fallback acp
- `tool-launchers.sh`: direct 未实现时打印 "direct 模式未实现，请配置 acp 模式"
- `tool-registry.toml`: 添加 `[tool.adapters]` 字段文档
