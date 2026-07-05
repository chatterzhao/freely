# PRD: adapter/ACP dispatch 注册表驱动化

## Goal
消除 tool-launchers.sh 中 adapter 查询、launch_kind、ACP dispatch、tool family 解析的硬编码 case 分支，改为从 tool-registry.toml 读取。使新增工具只需配置 TOML 即可通过 ACP 启动。

## Dev-Loop Handoff
1. tool_supported_adapters() → adapters.supported
2. tool_supported_launch_kinds_for_adapter() → adapters.launch_kinds.{adapter}
3. tool_run_acp_from_prompt_file() → 通用 ACP 参数构建路径
4. _resolve_tool_family() fallback → 扫描 registry aliases
5. tool_supports_add_dir_boundary() → launch.direct.add_dir_boundary
6. monitor-ai-acp.sh → 移除 hardcoded permission fallback

## Non-Goals
- 不迁移 direct 模式 case 分支
- 不改变 acp-bridge.py/run-acp-prompt.py 架构
