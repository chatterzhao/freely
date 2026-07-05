---
local_id: I-20260505T1210Z-A-B
issue_title: issue-sync 只写 platform_state，不碰 phase_state
kind: linked
phase_state: completed
promoted_from: raw-20260505T1210Z
platform_ids:
  github:
    issue_id: '214'
    url: https://github.com/chatterzhao/freely/issues/214
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/issue-state-refactor/issues/I-20260505T1210Z-A-B.md
created_at: '2026-05-05T12:10:02Z'
updated_at: '2026-05-17T08:02:22Z'
session_refs: []
platform_state: closed
---

## Scope

修正 bin/issue-sync 的 cmd_close 和 cmd_create：只更新 platform_state，不写 phase_state。

## 改动

- cmd_close: _fm_set_str platform_state closed（当前: _fm_set_str status closed）
- cmd_create: _fm_set_str platform_state open
