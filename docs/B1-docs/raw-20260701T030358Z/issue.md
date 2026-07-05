---
local_id: raw-20260701T030358Z58Z
kind: raw
phase_state: absorbed
absorbed_into: raw-20260701T030358Z58Z
platform_ids:
  github:
    issue_id: '3678'
    url: https://github.com/chatterzhao/freely/issues/3678
    synced_at: ''
  gitee:
    issue_id: IJY0AC
    url: https://gitee.com/zhaoquan/freely/issues/IJY0AC
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T03:04:18Z'
updated_at: '2026-07-01T03:04:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 问题

 已在  中声明忽略，但以下运行时文件在 gitignore 生效前就被提交，一直未被脱钩：

-  — 运行时配置，由 `freely init` 从 `templates/agent-table.toml.example` 释放
-  — 运行时状态文件

这导致 daemon 启动时修改这些文件会触发 "develop working tree is dirty" 错误。

## 根因

文件在  添加前就已存在于 git 历史中。已有模板路径：

- 模板: `templates/agent-table.toml.example` ✅ (git 跟踪)
- 运行时: `.freely/agent-table.toml` ❌ (不应跟踪)

## 修复

`git rm --cached` 两个文件，保留磁盘副本，同时把 `skip-worktree` 清理掉。
