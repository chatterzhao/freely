---
local_id: raw-20260510T1840Z
kind: raw
title: 'fix: remove init --skip-branch-check bypass'
phase_state: proposed
platform_ids:
  github:
    issue_id: '349'
    url: https://github.com/chatterzhao/freely/issues/349
    synced_at: '2026-05-15T18:24:39Z'
primary_platform: github
updated_at: '2026-05-15T18:24:39Z'
created_at: '2026-05-15T18:24:39Z'
platform_state: open
---
## 问题
init --skip-branch-check 可绕过分支校验，daemon start 不检查。
## 修复
移除 skip，init 和 daemon start 都强制检查，不绕过。
