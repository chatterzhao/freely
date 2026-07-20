---
local_id: raw-20260720T045011Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '4050'
    url: https://github.com/chatterzhao/freely/issues/4050
    synced_at: ''
  gitee:
    issue_id: IK294D
    url: https://gitee.com/zhaoquan/freely/issues/IK294D
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T04:50:34Z'
updated_at: '2026-07-20T04:50:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Root Cause
capture_worker_session_id_and_store() L13093 使用硬编码 UUID-only regex，拒绝 opencode 的 ses_ 格式 session ID。

is_valid_session_id() L4028 已同时支持 UUID 和 ses_ 格式，但 capture 函数未使用。

## Impact
Worker 实际在工作（cycle-worker log 有完整执行内容），但 Runtime 无法捕获 session ID：
- agent_working 不更新 session_id
- Runtime 认为 Worker "失败"
- Manager 看到 stale submitted → 重复委派（死循环）

## Fix
L13093 替换为 `is_valid_session_id "$_session_id"`
