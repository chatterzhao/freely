---
local_id: raw-20260617T042034Z34Z
kind: raw
- phase_state: absorbed
platform_ids:
  github:
    issue_id: '2886'
    url: https://github.com/chatterzhao/freely/issues/2886
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T04:20:50Z'
updated_at: '2026-06-17T04:20:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

B1 修复在 rebase 中丢失。monitor-ai-acp.sh L414-415 使用未定义的 $bridge_lost_marker / $network_failure_marker，应为 $bridge_lost_marker_file / $network_failure_marker_file。
