---
local_id: raw-20260701T054502Z02Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T054502Z-A
platform_ids:
  github:
    issue_id: '3688'
    url: https://github.com/chatterzhao/freely/issues/3688
    synced_at: ''
  gitee:
    issue_id: IJY1JM
    url: https://gitee.com/zhaoquan/freely/issues/IJY1JM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T05:45:24Z'
updated_at: '2026-07-01T05:45:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n
## 问题

governance-merge-gate 的 raw/C/M/I lifecycle 错误中，只有 4 个有 `→ 请阅读 skill:freely-doc-XX §门禁常见坑速查` 引导，其余关键错误缺失 skill 引用。

## 缺失 skill 引用的错误

- `promoted_issue_path is still 'missing'` → 应指向 B2_IBM
- `milestone binding is missing` → 应指向 B1_IBM
- `no valid source_candidate` → 应指向 B1_IBM
- `candidate_issues entry missing` → 应指向 B1_IBM
- `Still only in milestone candidate_issues` → 已有引用确认格式正确

## 修复

在 governance-merge-gate Python 脚本中，给每个 lifecycle 错误消息追加对应的 skill 引用。
