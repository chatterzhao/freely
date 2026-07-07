---
local_id: raw-20260707T043833Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3795'
    url: https://github.com/chatterzhao/freely/issues/3795
  gitee:
    issue_id: IJZBPS
primary_platform: github
canonical_issue_path: ''
created_at: '2026-07-07T04:38:33Z'
author: platform
channel: github
session_refs: []
---
## 问题
之前重构"只允许 platform"遗漏了多个本地 raw issue 创建路径，需要彻底清理。
## 预研发现
7 个文件包含本地 raw issue 路径（chat-inbox / freely.db new-issue / consumed=0 逻辑等）
