---
local_id: raw-20260601T025829Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2388'
    url: https://github.com/chatterzhao/freely/issues/2388
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-01T02:58:44Z'
updated_at: '2026-06-01T02:58:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 修复
1. file_mtime_epoch: stat -f %m (BSD/macOS) || stat -c %Y (GNU/Linux)
2. heartbeat stat 调用改用 file_mtime_epoch
3. monitor-ai-acp.sh _file_mtime_epoch 同上
4. _tool_test_resurrect: timeout(1) || perl alarm 双回退
