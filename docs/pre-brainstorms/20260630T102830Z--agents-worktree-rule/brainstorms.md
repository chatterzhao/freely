---
b1_id: B1-20260630T102830Z
phase_state: completed
source_raw: raw-20260630T102830Z
produced_candidate: C-20260630T102830Z-A
---

# B1: AGENTS.md 禁止 git worktree/branch deletion

## Problem
AGENTS.md line 235: `git worktree remove && git branch -d` 教人违规。
禁止操作节缺少对 git 原生命令删除的禁令。

## Decision
两个文件：AGENTS.md + AGENTS.md.example。替换违规示例，增加禁令。
