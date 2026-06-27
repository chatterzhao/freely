---
b1_id: B1-20260627T030447Z
phase_state: completed
source_raw: raw-20260627T030447Z
source_url: https://github.com/chatterzhao/freely/issues/3578
produced_candidate: C-20260627T030447Z-A
created_at: 2026-06-27
---

# B1_IBM: claude ACP adapter 不被支持 — 工具适配器注册表硬编码遗漏

## Input
- 来源: raw-20260627T030447Z (GitHub #3578)
- 症状: Freely daemon 启动后 manager 无法通过 ACP 启动 claude，报 "unsupported adapter 'acp' for tool 'claude' (supported: direct)"

## Problem
`tool_supported_adapters_for_runtime()` 硬编码了各工具的适配器支持列表，遗漏 `claude` 和 `cline`。
此外 `tool_default_adapter()` / `tool_default_adapter_for_runtime()` 也存在死代码（写死返回值），
`AI_TOOL_ADAPTER` 未导出导致 monitor 脚本选择错误。

## Brainstorm

### Option A: 追加遗漏的工具到硬编码列表
在 `tool_supported_adapters_for_runtime` 的 case 中加上 `claude|cline`。
- 优点: 改动最小
- 缺点: 每次加新工具都要改两处（TOML + bash case），维护负担

### Option B: 移除硬编码，全部从 registry 读取
`tool_supported_adapters_for_runtime` 改为调用 `_tool_registry_get` 读取 `adapters.supported`。
- 优点: 工具注册 TOML 成为唯一真相来源
- 缺点: 需要同时修复 `tool_default_adapter` 的 fallback 逻辑

## Decision: Option B
tool-registry.toml 已经声明了所有工具的 `adapters.supported` 和 `adapters.default`，
bash 代码不应该维护一份平行的硬编码列表。改为 registry 驱动后，新增工具只需在 TOML 注册。

## Candidate
- candidate_id: C-20260627T030447Z-A
- status: promoted
- milestone: M-20260627T030447Z-A
