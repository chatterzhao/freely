---
local_id: raw-20260626T142357Z57Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3561'
    url: https://github.com/chatterzhao/freely/issues/3561
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T14:24:18Z'
updated_at: '2026-06-26T14:24:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T142357Z-A
source_candidate: docs/B1-docs/raw-20260626T142357Z57Z/candidates.md#C-20260626T142357Z-A
platform_state: closed
---

## 问题

PR #3548 在 wt-close Phase 6b 加入 agent-id.env 清理时，`local _dev_wt` 声明在脚本主体内（非函数），导致运行时报错 `local: can only be used in a function`。

## 修复

去掉 `local` 关键字。
