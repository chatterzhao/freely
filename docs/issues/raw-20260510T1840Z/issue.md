---
local_id: raw-20260510T1840Z
kind: raw
phase_state: proposed
platform_ids: {}
primary_platform: ''
---
## 问题
init --skip-branch-check 可绕过分支校验，daemon start 不检查。
## 修复
移除 skip，init 和 daemon start 都强制检查，不绕过。
