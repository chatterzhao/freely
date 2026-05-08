---
local_id: raw-20260507T143546Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '249'
    url: https://github.com/chatterzhao/freely/issues/249
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T14:35:46Z'
updated_at: '2026-05-07T14:35:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
---

## 问题

当用户手动在 GitHub/Gitee 创建 issue 时，标题中的 raw key 可能缺秒或格式不规范。平台 API 返回的 `created_at` 是精确到秒的，可用于标准化。

## 修复

在 `platform-adapter.py pull_raw_issue()` 中，拿到平台 `created_at` 后与标题中的 key 比较，不一致则用平台 API 修正标题。
