---
local_id: raw-20260510T0856Z
kind: raw
phase_state: completed
platform_ids:
  github:
    issue_id: '272'
    url: https://github.com/chatterzhao/freely/issues/272
primary_platform: github
platform_state: closed
---
## 问题

wait→auto 切换后看门狗误杀 supervisor（竞态）。
## 修复

task_mode_gate 加 mode_just_switched 列，一次切换一次豁免。
