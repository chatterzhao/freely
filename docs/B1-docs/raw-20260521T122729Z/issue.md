---
local_id: raw-20260521T122729Z29Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '1917'
    url: https://github.com/chatterzhao/freely/issues/1917
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T12:27:41Z'
updated_at: '2026-06-21T20:12:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-05-21T15:26:59Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
platform_state: closed
absorbed_into: raw-20260710T005219Z---

## 问题
oc-acp-ds-flash-auto alias 展开为 OPENCODE_CONFIG=... opencode，但新的 _resolve_tool_family 用 expansion%% * 取第一个词（OPENCODE_CONFIG=...），而非最后一个词（opencode）。导致 binary 识别错误，adapter 检查失败。

## 修复
在 _resolve_tool_family 中恢复 env var stripping 逻辑：提取 expansion 后，先跳过 VAR=val 前缀，再取 binary。同时 _apply_tool_alias_settings 也需要相应的 env var 提取。
