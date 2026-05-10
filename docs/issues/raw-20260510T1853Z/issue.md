---
local_id: raw-20260510T1853Z
kind: raw
phase_state: proposed
platform_ids: {}
---
## 问题
init 分支校验只检查命名，不检查 worktree。提示缺少具体修复命令。
## 修复
1. 坏分支给出具体 git 命令（rename + 创建 fix worktree + 创建 test worktree）
2. 检查 fix/feature 分支是否缺少 worktree
