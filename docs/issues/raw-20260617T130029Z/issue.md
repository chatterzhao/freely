---
local_id: raw-20260617T130029Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T130029Z-A
platform_ids:
  github:
    issue_id: '2925'
    url: https://github.com/chatterzhao/freely/issues/2925
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T13:00:45Z'
updated_at: '2026-06-21T18:30:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

当前 git pull 冲突时只输出模糊信息，不列出冲突文件，不提供 abort 路径。

修复：输出 git 错误 + 冲突文件列表 + resolve 和 abort 两条路径。
