---
local_id: raw-20260719T133426Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T133426Z-A
platform_ids:
  github:
    issue_id: '4017'
    url: https://github.com/chatterzhao/freely/issues/4017
    synced_at: ''
  gitee:
    issue_id: IK222T
    url: https://gitee.com/zhaoquan/freely/issues/IK222T
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T13:34:50Z'
updated_at: '2026-07-19T13:34:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
freely L15684 manager_exit_contract_kind查--status pending, 但A2A task创建时state=submitted。pending是旧名, a2a_task.py有pending→submitted映射, 但Runtime直接写死pending字符串。

## 修复
L15684: --status pending → --status submitted
