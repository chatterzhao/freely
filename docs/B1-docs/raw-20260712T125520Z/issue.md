---
local_id: raw-20260712T125520Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260712T124601Z-A
platform_ids:
  github:
    issue_id: '3895'
    url: https://github.com/chatterzhao/freely/issues/3895
    synced_at: ''
  gitee:
    issue_id: IK0GNH
    url: https://gitee.com/zhaoquan/freely/issues/IK0GNH
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T12:55:55Z'
updated_at: '2026-07-12T12:55:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
--mode "$AI_MODE" 同样缺少默认值，导致 daemon fresh_with_handoff crash。

## 修复
$AI_MODE → ${AI_MODE:-wait}
