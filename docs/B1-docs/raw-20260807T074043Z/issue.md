---
schema_version: '1'
local_id: raw-20260807T074043Z
kind: raw
phase_state: dropped
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4099'
    url: https://github.com/chatterzhao/freely/issues/4099
    synced_at: ''
  gitee:
    issue_id: IK75S0
    url: https://gitee.com/zhaoquan/freely/issues/IK75S0
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T07:40:43Z'
updated_at: '2026-08-07T07:54:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-08-07T07:50:00Z'
closeout_note: cleanup raw without canonical absorber (final cleanup)
---

workflow_kind: fix

# chore: cleanup raw-20260807T073145Z 改 dropped（无吸收者）

## 现象
scan 报 raw-20260807T073145Z absorbed 缺 canonical（absorbed_into 指向未物化 I-*）。

## 修复方案
改 dropped + completed_at + closeout_note（cleanup 无吸收者语义，LAWS §304 豁免）。
