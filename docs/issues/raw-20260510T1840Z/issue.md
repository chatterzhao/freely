---
local_id: raw-20260510T1840Z
kind: raw
phase_state: completed
platform_ids:
  github:
    issue_id: '371'
    url: https://github.com/chatterzhao/freely/issues/371
    synced_at: '2026-05-16T13:21:00Z'
primary_platform: github
platform_state: open
updated_at: 2026-05-17T04:47:25Z
created_at: '2026-05-16T13:21:00Z'
---
## 问题
init --skip-branch-check 可绕过分支校验，daemon start 不检查。
## 修复
移除 skip，init 和 daemon start 都强制检查，不绕过。
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
