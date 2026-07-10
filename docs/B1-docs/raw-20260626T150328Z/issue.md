---
local_id: raw-20260626T150328Z28Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260626T150328Z-A
platform_ids:
  github:
    issue_id: '3563'
    url: https://github.com/chatterzhao/freely/issues/3563
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T15:03:59Z'
updated_at: '2026-06-26T15:03:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 根因

`tool-registry-query.py` line 111 输出 TOML 数组时用 `" ".join()` （空格连接），但 bash 端 `tool-launchers.sh` 的 `tool_supported_adapters` 等函数用 `tr ',' '\n'` 按逗号拆分。

例如 registry 中 `supported = ["direct", "acp"]`，Python 输出 `direct acp`（一行），bash grep -Fxq "acp" 失败 → 报错 `unsupported adapter 'acp' for tool '...' (supported: direct acp)`。

## 影响

- claude、opencode、codex 等所有注册工具的 acp adapter 校验全部失败
- AI cycle 立即 exit rc=1，触发 tool_unproductive → 不断切换到 fallback 工具
- Freely 完全无法启动 (daemon start 后 supervisor 立即退出)

## 修复方案

1. `tool-registry-query.py` line 111: `" ".join` → `",".join`（统一用逗号分隔）
2. `tool-launchers.sh` `_resolve_tool_by_binary`: `for _a in $_aliases` → `for _a in ${_aliases//,/ }`（适配逗号分隔的 aliases）

## 验证

`python3 tool-registry-query.py tool-registry.toml claude adapters.supported` 应输出 `direct,acp` 而非 `direct acp`
