---
local_id: raw-20260601T074306Z06Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2395'
    url: https://github.com/chatterzhao/freely/issues/2395
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-01T07:43:21Z'
updated_at: '2026-06-17T00:25:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
absorbed_into: raw-20260710T005219Z---

## 修复
1. dead threshold 3→2：1小时窗口内 opencode 900s 周期只能累积 2 次失败，永达不到 3
2. FREELY_ACP_FIRST_LAUNCH_DONE=0 在跨工具切换后重置：防止新工具 bridge 用旧 session ID resume 导致 idle timeout
