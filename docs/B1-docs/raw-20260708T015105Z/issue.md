---
local_id: raw-20260708T015105Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260708T015105Z-A'
platform_ids:
  github:
    issue_id: '3817'
    url: https://github.com/chatterzhao/freely/issues/3817
    synced_at: ''
  gitee:
    issue_id: IJZIZG
    url: https://gitee.com/zhaoquan/freely/issues/IJZIZG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T01:51:27Z'
updated_at: '2026-07-08T01:51:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 修复

1. freely_db_manager.py: #3796 删除 materialize 分支后留了悬空 elif → 改为 if
2. bin/issue-sync: cmd_close 删除 updated_at 写入，使 close 幂等

## 影响

1. DB daemon 启动失败（SyntaxError）
2. pr-merge-guarded issue-sync 死循环
