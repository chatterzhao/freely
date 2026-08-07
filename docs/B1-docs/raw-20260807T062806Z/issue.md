---
schema_version: '1'
local_id: raw-20260807T062806Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T062806Z-A
platform_ids:
  github:
    issue_id: '4090'
    url: https://github.com/chatterzhao/freely/issues/4090
    synced_at: ''
  gitee:
    issue_id: IK74PV
    url: https://gitee.com/zhaoquan/freely/issues/IK74PV
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T06:28:07Z'
updated_at: '2026-08-07T06:28:32Z'
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

# chore: 214 个 legacy absorbed raw 转 dropped + 2 个 cleanup raw 物化 I-*

## 现象
scan 报 214 个 2a_invalid_raw_metadata：180 个 absorbed raw 无 canonical id/path、17 个 canonical path 不存在、12 个 absorbed_into 非 I-*、5 个 strict raw 的 absorbed_into 指向未物化 I-*（20260807T053403Z、20260807T061132Z）。

## 根因
历史 legacy absorbed raw 无吸收者；cleanup 工位的 raw absorbed_into 指向未物化的 I-*。

## 修复方案
legacy absorbed raw 转 dropped（terminal 且无需 canonical）；为 2 个 cleanup raw 物化最小 I-* 文档（cleanup 类，LAWS §304 豁免路径）。
