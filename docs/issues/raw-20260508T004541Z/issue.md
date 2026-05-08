---
local_id: raw-20260508T004541Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: "250"
    url: https://github.com/chatterzhao/freely/issues/250
    synced_at: ""
primary_platform: github
canonical_issue_path: ""
last_synced_comment_at: {}
hash: ""
created_at: "2026-05-08T00:45:41Z"
updated_at: "2026-05-08T00:45:41Z"
intake_id: ""
author: platform
channel: github
session_refs: []
platform_state: open
---

## 背景

项目 skill 已部署到 ~/.claude/skills/，引用 skill 应使用 skill:name 而非路径。

## 改动

将 30 个文件中的路径引用改为 skill 名。
