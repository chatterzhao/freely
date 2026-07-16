---
local_id: raw-20260716T020008Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T020008Z-A
platform_ids:
  github:
    issue_id: '3923'
    url: https://github.com/chatterzhao/freely/issues/3923
    synced_at: ''
  gitee:
    issue_id: IK1CLI
    url: https://gitee.com/zhaoquan/freely/issues/IK1CLI
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T02:00:30Z'
updated_at: '2026-07-16T02:00:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
capture_worker_session_id_and_store 捕获 worker session_id 后只更新 A2A task，不写 agent_working。agent_assign 在 fork 前写了基本条目，但 session_id 从未回填。

## 修复
capture_worker_session_id_and_store 增加 target_project/agent_id/slot 参数，捕获 session_id 后调用 acp_session_register 更新 agent_working。
