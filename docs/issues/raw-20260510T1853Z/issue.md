---
local_id: raw-20260510T1853Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '376'
    url: https://github.com/chatterzhao/freely/issues/376
    synced_at: '2026-05-16T13:22:28Z'
platform_state: closed
updated_at: 2026-05-17T04:47:25Z
primary_platform: github
created_at: '2026-05-16T13:22:28Z'
---
## 问题
init 分支校验只检查命名，不检查 worktree。提示缺少具体修复命令。
## 修复
1. 坏分支给出具体 git 命令（rename + 创建 fix worktree + 创建 test worktree）
2. 检查 fix/feature 分支是否缺少 worktree
