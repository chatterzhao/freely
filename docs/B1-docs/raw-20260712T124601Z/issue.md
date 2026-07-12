---
local_id: raw-20260712T124601Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260712T124601Z-A
platform_ids:
  github:
    issue_id: '3893'
    url: https://github.com/chatterzhao/freely/issues/3893
    synced_at: ''
  gitee:
    issue_id: IK0GMB
    url: https://gitee.com/zhaoquan/freely/issues/IK0GMB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T12:46:23Z'
updated_at: '2026-07-12T12:46:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
line 20256: ${AI_MODE} 缺少默认值，session rotation 时 set -u 导致 unbound variable crash。

## 修复
${AI_MODE} → ${AI_MODE:-auto}
