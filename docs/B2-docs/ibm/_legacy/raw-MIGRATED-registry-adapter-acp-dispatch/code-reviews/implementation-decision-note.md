## Implementation Decision Note

- issue_id: I-20260624T090635Z-A
- issue_path: docs/issues/I-20260624T090635Z-A/issue.md
- decision: 6 个函数/位置的硬编码 case 分支改为 registry 驱动查询
- why_this: registry 已声明 adapters/launch_kinds/aliases/add_dir_boundary 全部字段，只差查询路径。registry 优先 + 最小保守 fallback 消除硬编码，使新增工具只需配 TOML 即可通过 ACP 启动
- alternatives_considered:
  1. 逐个迁移保留 fallback — 两边维护，硬编码不消失
  2. 全面移除硬编码 — 需要全面回归测试
  3. registry 优先 + 保守默认（选用）— 注册命中走 registry，未命中走安全默认
- boundary_non_goals: 不迁移 direct 模式（DEPRECATED），不改变 acp-bridge 架构，不迁移 ai-cli
- residual_risk:
  - codex 独立 bridge socket 路径保留，不受通用化影响
  - 未注册工具走 direct-only（保守），需显式注册才能用 ACP
  - Cline 等新工具需要 registry 中有完整 [tool.acp] 段才能正常工作

### Changes
1. tool_supported_adapters() → _tool_registry_get adapters.supported
2. tool_supported_launch_kinds_for_adapter() → _tool_registry_get adapters.launch_kinds.{adapter}
3. tool_run_acp_from_prompt_file() → 合并 claude/opencode 为通用路径, codex 保留独立, *) 不再报错
4. _resolve_tool_family() → 新增 _resolve_tool_by_binary 扫描 registry aliases
5. tool_supports_add_dir_boundary() → _tool_registry_get launch.direct.add_dir_boundary
6. monitor-ai-acp.sh → 移除 case claude/codex/opencode 硬编码, warn 替代 error
