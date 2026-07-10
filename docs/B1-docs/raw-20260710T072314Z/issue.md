---
local_id: raw-20260710T072314Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T072314Z-A
platform_ids:
  github:
    issue_id: '3869'
    url: https://github.com/chatterzhao/freely/issues/3869
    synced_at: ''
  gitee:
    issue_id: IK068Q
    url: https://gitee.com/zhaoquan/freely/issues/IK068Q
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T07:23:37Z'
updated_at: '2026-07-10T07:23:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

_send_request 中的 session/prompt idle check 和 _idle_monitor_loop 双重 idle 检测互相冲突：
1. session/prompt 等待期间 AI 思考无 stdout → _send_request 内联 idle check 触发 → 弹出 pending 条目
2. _idle_monitor_loop 检查 pending → 已空 → 触发 bridge shutdown
3. Manager AI 被 SIGTERM 杀死 (rc=143)

PR #3868 只修复了 _idle_monitor_loop，但 _send_request 的内联 idle check 在更早的阶段就杀死了 prompt。

## 修复

移除 _send_request 中 session/prompt 的内联 idle check。Idle 检测统一由 _idle_monitor_loop（bridge 级，检查 has_active_prompt）负责。prompt 只保留绝对超时 BRIDGE_TIMEOUT(1800s) 作为 safety net。

## 验收

Manager cycle 不再被 rc=143 杀死。
