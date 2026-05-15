---
local_id: raw-20260510T1853Z
kind: raw
title: 'fix: init branch check should also verify worktree'
phase_state: proposed
platform_ids:
  github:
    issue_id: '350'
    url: https://github.com/chatterzhao/freely/issues/350
    synced_at: '2026-05-15T18:24:44Z'
updated_at: '2026-05-15T18:24:44Z'
primary_platform: github
created_at: '2026-05-15T18:24:44Z'
platform_state: open
---
## 问题
init 分支校验只检查命名，不检查 worktree。提示缺少具体修复命令。
## 修复
1. 坏分支给出具体 git 命令（rename + 创建 fix worktree + 创建 test worktree）
2. 检查 fix/feature 分支是否缺少 worktree
