---
schema_version: '1'
local_id: raw-20260807T074857Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260807T074857Z-A'
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4101'
    url: https://github.com/chatterzhao/freely/issues/4101
    synced_at: ''
  gitee:
    issue_id: IK75UW
    url: https://gitee.com/zhaoquan/freely/issues/IK75UW
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T07:48:57Z'
updated_at: '2026-08-07T07:49:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

# chore: cleanup raw-20260807T074043Z 改 dropped（收尾）

## 现象
scan 报 raw-20260807T074043Z absorbed 缺 canonical。

## 修复方案
改 dropped + completed_at + closeout_note（cleanup 无吸收者统一语义）。
