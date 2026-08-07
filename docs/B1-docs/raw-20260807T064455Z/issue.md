---
schema_version: '1'
local_id: raw-20260807T064455Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4093'
    url: https://github.com/chatterzhao/freely/issues/4093
    synced_at: ''
  gitee:
    issue_id: IK74WN
    url: https://gitee.com/zhaoquan/freely/issues/IK74WN
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T06:44:55Z'
updated_at: '2026-08-07T06:45:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

## 现象
scan 报 20 个 2a_state_mismatch（terminal 但 platform_state=open）与 6 个 2a_invalid_raw_metadata（strict raw absorbed 缺 completed_at）。

## 修复方案
20 个 legacy raw 的 platform_state 改 closed；6 个 strict raw 补 completed_at（cleanup 类，LAWS §304 豁免路径）。
