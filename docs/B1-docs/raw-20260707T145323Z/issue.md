---
local_id: raw-20260707T145323Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260707T145323Z-A
platform_ids:
  github:
    issue_id: '3809'
    url: https://github.com/chatterzhao/freely/issues/3809
    synced_at: ''
  gitee:
    issue_id: IJZHK8
    url: https://gitee.com/zhaoquan/freely/issues/IJZHK8
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T14:53:46Z'
updated_at: '2026-07-07T15:21:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

issue-sync close 每次都写 `updated_at: $(date)`。第二次跑 timestamp 变了 → git 检测 diff → 产生 commit → pr-merge-guarded dev↔test 不一致 → 重跑又产生新 commit → 死循环。

## 修复

删掉 `cmd_close` 中的 `_fm_set_str updated_at` 行。`platform_state: closed` 是幂等的——重写相同值 git 不会检测到变化。

## 改动

bin/issue-sync: 删除 1 行
