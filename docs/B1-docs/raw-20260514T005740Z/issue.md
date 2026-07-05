---
local_id: raw-20260514T005740Z40Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260514T005740Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-17T00:22:40Z'
platform_ids:
  github:
    issue_id: '340'
    url: https://github.com/chatterzhao/freely/issues/340
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-14T00:57:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260514T005740Z40Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260514T005740Z40Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-14T00:57:40Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260514T005740Z40Z`。实现前请用 `wt-create --raw-key 20260514T005740Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
status: open
source: chat-inbox
created_at: "2026-05-14T00:57:40Z"
title: "fix: alias resolution strips env var prefix — generalize _resolve_tool_family + _apply_tool_alias_settings"

## 问题

别名 `oc-run-ds-flash-auto='OPENCODE_CONFIG=... opencode run --print-logs'` 以环境变量开头。
`_resolve_tool_family` 提取第一个词作为二进制，拿到的是 `OPENCODE_CONFIG=...`（不是 `opencode`）。
导致需要硬编码到 5 个位置才能工作，违背了“任意 alias 不需改代码”的设计意图。

对比 `cc-ds-flash-auto='claude --settings ...'` 以裸二进制开头，完全不需要硬编码。

## 需要修复的缺口

### A. _resolve_tool_family — 剥离 env 前缀

`_resolve_tool_family()`（tool-launchers.sh + freely runtime）中，alias 解析后应剥离前导的 `ENV_VAR=value` 赋值，再提取二进制名。

### B. _apply_tool_alias_settings — 导出 env 前缀

`_apply_tool_alias_settings()` 只理解 `--settings <path>` 模式。需要从 alias 中提取 `ENV_VAR=value` 前缀并 `export`。

### C. 直接模式内联 _resolve_tool_alias — 同样修复

`tool_run_direct_from_prompt_file` 内的内联解析也有相同问题。

## 修复后

从所有 5 个硬编码位置移除 `oc-run-ds-flash-auto`，通用路径自动处理它。
`oc-ds-flash-auto` 和任何 `ENV_VAR=val binary` 格式的 alias 都不需要硬编码。

## 改动范围

- EDIT: docs/system/workspace/scripts/runtime/tool-launchers.sh（_resolve_tool_family, _apply_tool_alias_settings, 内联 _resolve_tool_alias, 移除硬编码）
- EDIT: docs/system/workspace/scripts/runtime/freely（_resolve_tool_family, tool_supported_adapters_for_runtime, 移除硬编码）
- 零新增 LOC，纯重构
