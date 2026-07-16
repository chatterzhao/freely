---
local_id: raw-20260716T103343Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3940'
    url: https://github.com/chatterzhao/freely/issues/3940
    synced_at: ''
  gitee:
    issue_id: IK1JNE
    url: https://gitee.com/zhaoquan/freely/issues/IK1JNE
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T10:34:05Z'
updated_at: '2026-07-16T10:34:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
PR #3939 的 agent_working writeback 使用 db-daemon RPC，但 AI cycle 完成后 db-daemon 常已重启导致 socket 不可用。loop log 显示 6 次 session upsert failed。

## 修复
改用普通文件 .freely/run/last-acp-session-id 存储真 session ID，零外部依赖。
