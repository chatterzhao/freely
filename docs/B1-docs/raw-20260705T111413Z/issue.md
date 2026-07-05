---
local_id: raw-20260705T111413Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T111413Z-A
platform_ids:
  github:
    issue_id: '3750'
    url: https://github.com/chatterzhao/freely/issues/3750
    synced_at: ''
  gitee:
    issue_id: IJYV0L
    url: https://gitee.com/zhaoquan/freely/issues/IJYV0L
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T11:14:39Z'
updated_at: '2026-07-05T11:14:39Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
projects.tsv 误入 repo 根目录（应位于 ~/.freely/）。该文件是机器相关的全局状态，记录已注册项目路径，不应提交。

## 修复
1. 删除 repo 根目录的 projects.tsv
2. 加入 .gitignore
