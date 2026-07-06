---
local_id: I-20260318-1630
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260318-1630/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '19'
    url: https://github.com/chatterzhao/freely/issues/19
    synced_at: '2026-04-27T11:13:47Z'
  gitee:
    issue_id: IJFO5C
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5C
    synced_at: '2026-04-27T13:14:03Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md
last_synced_comment_at:
  github: '2026-04-27T11:13:47Z'
hash: ''
created_at: '2026-04-27T11:13:47Z'
updated_at: '2026-04-27T11:13:47Z'
platform_state: closed
---

一旦 future global `restart` 成为显式 all-project control-plane action，Freely 不能只做 blind kill + blind relaunch。它必须记住 restart 前哪些 projects 处于 running，保留恢复所需的 durable evidence，并显式排除 operator 已停下的 projects。

canonical: docs/B2-docs/ibm/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md
