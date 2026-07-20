---
local_id: raw-20260720T051323Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '4052'
    url: https://github.com/chatterzhao/freely/issues/4052
    synced_at: ''
  gitee:
    issue_id: IK296J
    url: https://gitee.com/zhaoquan/freely/issues/IK296J
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T05:13:47Z'
updated_at: '2026-07-20T05:13:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Root Cause
capture_worker_session_id_and_store() L13093 使用硬编码 UUID regex，拒绝 opencode 的 ses_ 格式 session ID。

is_valid_session_id() L4028 已同时支持 UUID 和 ses_ 格式，但 capture 未使用。

## Impact
Worker 实际在工作但 Runtime 无法捕获 session ID → agent_working 不更新 → Runtime 误判 Worker 失败 → Manager 重复委派死循环。

## Fix
L13093: 硬编码 regex → is_valid_session_id "$session_id"
