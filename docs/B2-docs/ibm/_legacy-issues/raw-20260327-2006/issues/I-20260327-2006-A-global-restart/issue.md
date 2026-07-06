---
local_id: I-20260327-2006-A-global-restart
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260327-2006/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '64'
    url: https://github.com/chatterzhao/freely/issues/64
    synced_at: '2026-04-27T11:20:57Z'
  gitee:
    issue_id: IJFO72
    url: https://gitee.com/zhaoquan/freely/issues/IJFO72
    synced_at: '2026-04-27T13:15:10Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:20:57Z'
hash: ''
created_at: '2026-04-27T11:20:57Z'
updated_at: '2026-05-17T08:01:31Z'
platform_state: closed
---

一旦 future global `restart` 成为显式 all-project control-plane action，Freely 不能只做 blind kill + blind relaunch。它必须记住 restart 前哪些 projects 处于 running，保留恢复所需的 durable evidence，并显式排除 operator 已停下的 projects。

canonical: docs/B2-docs/ibm/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md
