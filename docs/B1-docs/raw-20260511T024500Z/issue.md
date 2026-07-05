---
local_id: raw-20260511T024500Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '374'
    url: https://github.com/chatterzhao/freely/issues/374
    synced_at: '2026-05-16T13:21:56Z'
platform_state: closed
updated_at: 2026-05-17T04:47:25Z
primary_platform: github
created_at: '2026-05-16T13:21:56Z'
---
## 问题
freely.db 路径构造分散在 19 处，格式不统一。
## 修复
抽出 project_db_path()，所有地方统一调用。
