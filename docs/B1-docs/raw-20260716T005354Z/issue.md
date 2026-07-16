---
local_id: raw-20260716T005354Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T005354Z-A
platform_ids:
  github:
    issue_id: '3921'
    url: https://github.com/chatterzhao/freely/issues/3921
    synced_at: ''
  gitee:
    issue_id: IK1BTL
    url: https://gitee.com/zhaoquan/freely/issues/IK1BTL
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T00:54:16Z'
updated_at: '2026-07-16T00:54:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
Worker launch bypasses acp_session_connect. acp_session_register skips non-manager.

## 修复
1. Worker launch via acp_session_connect (cross-tool→new+log)
2. acp_session_register writes for worker/reviewer
