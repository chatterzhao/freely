---
schema_version: '1'
local_id: raw-20260807T075642Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T075642Z-A
platform_ids:
  github:
    issue_id: '4103'
    url: https://github.com/chatterzhao/freely/issues/4103
    synced_at: ''
  gitee:
    issue_id: IK760H
    url: https://gitee.com/zhaoquan/freely/issues/IK760H
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T07:56:42Z'
updated_at: '2026-08-07T08:04:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-08-07T07:55:00Z'
closeout_note: ''
---

workflow_kind: fix

# chore: cleanup raw-20260807T074857Z 改 dropped（终结）

## 现象
scan 报 raw-20260807T074857Z absorbed 缺 canonical（cleanup 工位模板缺陷：cleanup raw 应 dropped 而非 absorbed）。

## 修复方案
改 dropped + completed_at + closeout_note。
