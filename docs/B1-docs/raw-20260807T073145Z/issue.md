---
schema_version: '1'
local_id: raw-20260807T073145Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260807T073145Z-A'
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4097'
    url: https://github.com/chatterzhao/freely/issues/4097
    synced_at: ''
  gitee:
    issue_id: IK75MM
    url: https://gitee.com/zhaoquan/freely/issues/IK75MM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T07:31:45Z'
updated_at: '2026-08-07T07:32:10Z'
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

# chore: scan 修复后暴露的 12 个 raw/I-* 状态补齐

## 现象
scan parse_frontmatter 修复后暴露真实状态：4 个 strict raw absorbed 缺 completed_at/canonical，8 个 I-* phase_state 为空。

## 修复方案
4 个 strict raw 补 completed_at（保持字段顺序）；8 个 I-* 标 dropped（legacy 无字段）（cleanup 类，LAWS §304 豁免路径）。
