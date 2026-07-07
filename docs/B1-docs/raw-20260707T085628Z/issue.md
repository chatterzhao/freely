---
local_id: raw-20260707T085628Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260707T085628Z-A
platform_ids:
  github:
    issue_id: '3801'
    url: https://github.com/chatterzhao/freely/issues/3801
    synced_at: ''
  gitee:
    issue_id: IJZEZ3
    url: https://gitee.com/zhaoquan/freely/issues/IJZEZ3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T08:56:49Z'
updated_at: '2026-07-07T09:09:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

当前 commands.md 写"执行位置: 项目根目录（develop）"等，但没有给出具体的 cd 命令。由于 Freely 自动创建 worktree 后会提示 cd 进入，文档应该使用一致的 cd 路径表述。

## 修复

每个命令的"执行位置"改为带 cd 路径的表述：
- feedback: cd <project-root>
- wt-create: cd <project-root>（develop 工位）
- pr-create-guarded: cd <fix-or-feature-worktree>（wt-create 输出的工位路径）
- pr-review-guarded: 任意工位
- pr-merge-guarded: cd <project-root>（develop 工位）
- wt-close: cd <project-root>
- develop-push: cd <project-root>
- issue-sync: cd <fix-or-feature-worktree>（禁止在保护分支）
- deploy-skills: cd <project-root>
- live/fleet-status: 任意工位
