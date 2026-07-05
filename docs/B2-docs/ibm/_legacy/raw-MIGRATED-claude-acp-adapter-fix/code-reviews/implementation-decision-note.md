---
issue_id: I-20260627T030447Z-A
issue_path: docs/issues/I-20260627T030447Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260627T030447Z-A
- issue_path: docs/issues/I-20260627T030447Z-A/issue.md

## Implementation Decision Note

- decision: 将 `tool_supported_adapters_for_runtime()` 和两个 `tool_default_adapter*` 函数从硬编码改为从 tool-registry.toml 读取 `adapters.supported` / `adapters.default`
- why_this: TOML 已经是单一真相来源，bash 不应维护平行硬编码列表。每次新增工具只需在 TOML 注册，无需改 bash
- alternatives_considered: 追加 `claude|cline` 到硬编码列表（改动最小但维护负担持续累积）
- boundary_non_goals: 不移除 `tool_run_direct_from_prompt_file` 中的 per-tool CLI 启动逻辑（那是 direct 模式的实现，不属于适配器注册表范畴）
- residual_risk: 如果某个工具的 TOML 配置缺少 `adapters.supported` 字段，会保守回退到 `direct`（符合 fail-safe 原则，不阻塞启动）
