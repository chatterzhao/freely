---
local_id: raw-20260627T084551Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3586'
    url: https://github.com/chatterzhao/freely/issues/3586
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T084551Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T08:46:12Z'
updated_at: '2026-06-27T08:46:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Scope

run-acp-prompt.py fork 路径从 session/new 改为 session/fork（ACP 官方规范方法），继承 parent 完整历史 → 缓存命中。

实测：Claude + OpenCode 支持 session/fork，Cline + Codex 不支持。try session/fork → 降级 session/new。

附带 Bug G: ensure-codex-acp 引用已删除的 tool-registry.json5。

## Changes

- run-acp-prompt.py: fork 路径 try session/fork → 降级 session/new
- ensure-codex-acp: .json5 → .toml
