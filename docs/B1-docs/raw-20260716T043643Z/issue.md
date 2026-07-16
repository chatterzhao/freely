---
local_id: raw-20260716T043643Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3934'
    url: https://github.com/chatterzhao/freely/issues/3934
    synced_at: ''
  gitee:
    issue_id: IK1EOK
    url: https://gitee.com/zhaoquan/freely/issues/IK1EOK
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T04:37:06Z'
updated_at: '2026-07-16T04:37:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
a2a_server.py POST /tasks handler (创建新 task) 未将 reason 字段写入数据库。虽然 PATCH handler 已正确处理 reason，但 a2a-exit 无 --task-id 创建新 task 时 reason 会丢失。

## 修复
在 POST handler 的 fields dict 中添加 reason: body.get("reason", "")

## 关联
这是 fix/raw-20260716T040152Z-agent-orchestration-fix 的补充修复。
