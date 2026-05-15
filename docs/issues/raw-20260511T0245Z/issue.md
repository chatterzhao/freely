---
local_id: raw-20260511T0245Z
kind: raw
title: 'fix: unify freely.db path construction across all callers'
phase_state: proposed
platform_ids:
  github:
    issue_id: '351'
    url: https://github.com/chatterzhao/freely/issues/351
    synced_at: '2026-05-15T18:24:50Z'
updated_at: '2026-05-15T18:24:50Z'
primary_platform: github
created_at: '2026-05-15T18:24:50Z'
platform_state: open
---
## 问题
freely.db 路径构造分散在 19 处，格式不统一。
## 修复
抽出 project_db_path()，所有地方统一调用。
