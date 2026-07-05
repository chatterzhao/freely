---
local_id: raw-20260624T062756Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T062756Z-A
platform_ids:
  github:
    issue_id: '3407'
    url: https://github.com/chatterzhao/freely/issues/3407
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T06:28:17Z'
updated_at: '2026-06-24T06:28:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象
docs/system/workspace/tools.md:39 仍引用旧名 tool-registry.json5，应改为 tool-registry.toml。

## 修复
```diff
- 当前 canonical ACP family 来自 `tool-registry.json5`
+ 当前 canonical ACP family 来自 `tool-registry.toml`
```
