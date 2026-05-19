---
local_id: I-20260327-2006-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '63'
    url: https://github.com/chatterzhao/freely/issues/63
    synced_at: '2026-04-27T11:20:51Z'
  gitee:
    issue_id: IJFO71
    url: https://gitee.com/zhaoquan/freely/issues/IJFO71
    synced_at: '2026-04-27T13:15:09Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:20:51Z'
hash: ''
created_at: '2026-04-27T11:20:51Z'
updated_at: '2026-05-17T08:01:29Z'
platform_state: closed
---

一旦 future global `restart` 成为显式 all-project control-plane action，Freely 不能只做 blind kill + blind relaunch。它必须记住 restart 前哪些 projects 处于 running，保留恢复所需的 durable evidence，并显式排除 operator 已停下的 projects。

canonical: docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md
