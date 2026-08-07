---
schema_version: '1'
local_id: raw-20260807T061132Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T061132Z-A
platform_ids:
  github:
    issue_id: '4087'
    url: https://github.com/chatterzhao/freely/issues/4087
    synced_at: ''
  gitee:
    issue_id: IK74EQ
    url: https://gitee.com/zhaoquan/freely/issues/IK74EQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T06:11:32Z'
updated_at: '2026-08-07T06:11:57Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-08-07T07:30:00Z'
closeout_note: ''
---

workflow_kind: fix

# chore: 51 个历史 raw/I-* phase_state 批量收尾为 terminal

## 现象
scan 持续报 51 个 2a_non_terminal：36 个历史 raw issue 的 phase_state 为 completed/proposed/open（raw terminal 应为 absorbed/dropped），15 个 I-* issue 为 in_dev/in_b2_ibm/done_b2_ibm/in_verification。对应平台 issue 均已 CLOSED。

## 根因
2026-05/06 批量 closeout 时代的历史状态未收敛为 terminal。

## 修复方案
批量将 raw phase_state 修正为 absorbed、I-* 修正为 completed（cleanup 类，LAWS §304 豁免路径）。
