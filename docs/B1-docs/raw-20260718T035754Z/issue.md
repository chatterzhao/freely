---
local_id: raw-20260718T035754Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260718T035754Z-A
created_at: 2026-07-18 03:57:54+00:00
author: zhaoquan
channel: freely-workflow-guarded-execution
platform_state: closed
---

## 根因
config.toml 中 FREELY_ACP_*_BIN 四个 key 全为空字符串。原因：
1. config.toml 是直接从模板 cp 而来，`freely init` 从未运行
2. 即使运行 init，`cmd_init()` 的 tool_adapter 解析通过 agent-table 体系（`project_tool_selection_truth`→读 `AGENT_AI_TOOL_ADAPTER` 空→policy=direct），`tool_adapter != "acp"` → `_init_acp_tool_setup()` 被跳过
3. bridge 启动时通过 `command -v` PATH fallback 能发现 binary，但发现后不回写 config.toml

## 影响
- 每次启动重新搜索 PATH
- worker 在工位（PATH 可能不含 nvm bin）启 bridge 时找不到
- `freely init` 即使 adapter 已配为 acp 也不会自动填充

## 修复方案
bridge 启动时 `command -v` 发现 binary 后**自动 `upsert_config_key` 回写** config.toml（自愈）。不改 resolution 链——build 时写入 1 次，后续启动直接读缓存。
