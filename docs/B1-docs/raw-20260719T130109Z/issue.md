---
local_id: raw-20260719T130109Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T130109Z-A
platform_ids:
  gitee:
    issue_id: IK21ZB
    url: https://gitee.com/zhaoquan/freely/issues/IK21ZB
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T21:01:39+08:00'
updated_at: '2026-07-19T21:01:39+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 根因
L13331 _worker_slot=AGENT_AI_TOOL(Manager的tool claude), 导致agent_working.slot写错

## 修复
改为agent-table-query --get-slot worker_01解析Worker的真实slot(opencode)
