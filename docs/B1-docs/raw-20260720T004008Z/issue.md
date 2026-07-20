---
local_id: raw-20260720T004008Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T004008Z-A
platform_ids:
  github:
    issue_id: '4031'
    url: https://github.com/chatterzhao/freely/issues/4031
    synced_at: ''
  gitee:
    issue_id: IK25QY
    url: https://gitee.com/zhaoquan/freely/issues/IK25QY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T00:40:31Z'
updated_at: '2026-07-20T00:40:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
freely L13347: --launch-kind fork 硬编码。跨tool时(Manager=claude, Worker=opencode)fork发到opencode bridge找不到parent session→超时。

## 修复
L13343前加判断: _worker_base == _mgr_base → fork, 否则→new
