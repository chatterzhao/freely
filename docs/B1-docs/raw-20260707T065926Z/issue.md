---
local_id: raw-20260707T065926Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260707T065926Z-A'
platform_ids:
  github:
    issue_id: '3799'
    url: https://github.com/chatterzhao/freely/issues/3799
    synced_at: ''
  gitee:
    issue_id: IJZDCX
    url: https://gitee.com/zhaoquan/freely/issues/IJZDCX
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T06:59:47Z'
updated_at: '2026-07-07T06:59:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

commands.md 没有标注每个命令必须在哪个工位/分支执行，导致用户在错误位置运行命令时报错。

## 源码中的工位要求

| 命令 | 执行位置 | 原因 |
|------|---------|------|
| feedback | 项目根目录（任意可写工位） | 创建平台 issue |
| wt-create | 项目根目录（develop） | 创建 worktree |
| pr-create-guarded | **必须在 fix/raw-* 或 feature/raw-* 工位** | 拒绝在 develop 执行 |
| pr-review-guarded | 任意工位 | 审查分支代码 |
| pr-merge-guarded | **必须在 develop** | 执行合并到 develop |
| wt-close | 项目根目录（develop） | 清理工位 |
| develop-push | 项目根目录（develop） | 推送 develop |
| issue-sync | **禁止在保护分支**（main/develop/test-pre-merge-*） | 防止污染 |
| deploy-skills | 项目根目录 | 部署 skills |
| live/fleet-status | 任意工位 | 只读状态查询 |

## 修复

在 commands.md 每个命令的详细说明中增加「执行位置」字段。
