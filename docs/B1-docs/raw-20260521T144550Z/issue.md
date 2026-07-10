---
local_id: raw-20260521T144550Z50Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2066'
    url: https://github.com/chatterzhao/freely/issues/2066
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T14:46:05Z'
updated_at: '2026-05-21T15:27:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-21T15:27:32Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: raw-20260710T005219Z---

## 问题
run-acp-prompt.py 第397-407行在每次session/new或session/resume后发送 session/set_mode bypassPermissions。acp-bridge.py已修复，但prompt客户端仍有残留。导致opencode仍然报Internal error。

## 修复
删除 run-acp-prompt.py:397-407 的bypassPermissions注入代码块。
