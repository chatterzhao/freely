---
local_id: raw-20260630T102830Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T102830Z-A
platform_ids:
  github:
    issue_id: '3651'
    url: https://github.com/chatterzhao/freely/issues/3651
    synced_at: ''
  gitee:
    issue_id: IJXWM8
    url: https://gitee.com/zhaoquan/freely/issues/IJXWM8
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T10:29:03Z'
updated_at: '2026-06-30T10:29:03Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

AGENTS.md 当前有两个问题：

1. **Line 235 教人违规**: `git worktree remove ../.../ && git branch -d <branch>` — 直接在“基本命令”里建议用 git 原生命令删除工位和分支，与 hook 保护机制冲突

2. **“禁止操作”节不全**: 缺少对 `git worktree remove`、`git branch -d/-D`、`rm -rf` 的明确禁令

## 改动

1. 从基本命令中删除 line 235 的 git 原生命令示例
2. 在禁止操作中加入 worktree/分支删除规则：
   - worktree 或分支禁止直接用 git 命令删除
   - 必须用 `freely wt-close` 收口（验 phase_state → 关平台 issue → 删 worktree → 删分支）
   - 引用 `freely wt-close --help` 查看完整用法
3. 在基本命令中增加 `freely wt-close` 入口
