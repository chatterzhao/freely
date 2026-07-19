---
local_id: raw-20260719T190945Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T190945Z-A
platform_ids:
  github:
    issue_id: '4023'
    url: https://github.com/chatterzhao/freely/issues/4023
    synced_at: ''
  gitee:
    issue_id: IK25J4
    url: https://gitee.com/zhaoquan/freely/issues/IK25J4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T19:10:08Z'
updated_at: '2026-07-19T19:10:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
governance-merge-gate.py is_governance_only_path(): L334-361硬编码14个路径 + L363-367读config做并集。config有值时应该是唯一权威源，不应与硬编码合并。

## 修复
config存在且非空时,只用config路径; config为空时fallback到硬编码默认
