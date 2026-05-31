---
local_id: raw-20260531T043558Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2367'
    url: https://github.com/chatterzhao/freely/issues/2367
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T04:36:12Z'
updated_at: '2026-05-31T04:36:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题
_tool_switch_launch_kind 在同工具但记录中 new_session_id 为空时总是返回 fresh，
导致每轮都是 fresh_with_handoff，从不进入 prompt 模式，零缓存命中。

根因：bridge 启动时 _tool_switch_atomic_write 会创建空 sid 新记录，
覆盖掉刚 writeback 的有效 session ID。

## 修复
_tool_switch_launch_kind 在记录无 sid 时 fallback 到 session-store：
有活跃 session → resume（允许 prompt 模式）
