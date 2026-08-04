---
local_id: raw-20260720T052911Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T052911Z-A
platform_ids:
  github:
    issue_id: '4054'
    url: https://github.com/chatterzhao/freely/issues/4054
    synced_at: ''
  gitee:
    issue_id: IK2997
    url: https://gitee.com/zhaoquan/freely/issues/IK2997
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T05:29:37Z'
updated_at: '2026-07-20T05:29:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

14 个 raw issue 的代码已合并到 develop，但平台 issue（GitHub/Gitee）仍处于 open 状态，未同步关闭。

## 影响

scan 持续报告 merged_develop 阶段条目，污染待办视图；平台 issue 状态与本地真相不一致。

## 修复方案

worker 对每个 raw key 执行：issue-sync close → git commit → wt-close。共 14 个 key：20260506T100000Z, 20260517T113021Z, 20260517T113514Z, 20260517T113807Z, 20260517T114147Z, 20260517T114702Z, 20260517T115113Z, 20260517T115824Z, 20260517T120124Z, 20260517T120752Z, 20260517T121432Z, 20260527T004453Z, 20260617T035314Z, 20260714T021808Z
