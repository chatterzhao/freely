---
local_id: raw-20260511T0245Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '374'
    url: https://github.com/chatterzhao/freely/issues/374
    synced_at: '2026-05-16T13:21:56Z'
platform_state: open
updated_at: '2026-05-16T13:21:56Z'
primary_platform: github
created_at: '2026-05-16T13:21:56Z'
---
## 问题
freely.db 路径构造分散在 19 处，格式不统一。
## 修复
抽出 project_db_path()，所有地方统一调用。
