---
local_id: I-20260503-0200-A
issue_title: 'scan: switch to task-lifecycle-scan v2 with full lifecycle chain trace'
kind: linked
phase_state: completed
completed_at: "2026-05-19T23:20:00Z"
absorbed_at: '2026-05-16T14:27:11Z'
promoted_from: raw-20260503-0200
platform_ids:
  github:
    issue_id: '227'
    url: https://github.com/chatterzhao/freely/issues/227
    synced_at: '2026-05-05T15:07:57Z'
  gitee:
    issue_id: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/scan-lifecycle-migration/issues/I-20260503-0200-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-03T02:00:00Z'
updated_at: '2026-05-17T12:25:18Z'
session_refs:
- tool: ccds
  session_id: 20260503-scan-lifecycle
  role: author
platform_state: closed
---

## Pre-Brainstorm Summary

废弃的 task-source-scan.py 输出147条噪声。新版 task-lifecycle-scan.py 已实现但从未接入 runtime。
切换到 v2：完整生命周期链条追踪（12 mandatory + 2 optional stations），Phase 0 信号扫描，
分支命名规范强制，AF_UNIX socket 路径修复。

## Scope

- task-lifecycle-scan.py: chain trace, chat inbox scan, governance scan
- freely: prompt builder 重写为 lifecycle-aware 输出
- acp-bridge.py: hash-based socket path
- wt-create: fix regex + test-pre-merge support
- pre-push.sh: branch naming gate
- .githooks/post-checkout: auto pre-init-runtime
