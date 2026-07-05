---
local_id: I-20260417-0445-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '151'
    url: https://github.com/chatterzhao/freely/issues/151
    synced_at: '2026-04-27T11:27:54Z'
  gitee:
    issue_id: IJFOA3
    url: https://gitee.com/zhaoquan/freely/issues/IJFOA3
    synced_at: '2026-04-27T13:17:24Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:27:54Z'
hash: ''
created_at: '2026-04-27T11:27:54Z'
updated_at: '2026-05-17T12:24:38Z'
platform_state: closed
---

Live process inspection showed the runtime leak was not one isolated leftover pid. The bounded defect was that user-facing start semantics, startup lock truth, same-project watcher discovery, and AI failure cleanup were still loose enough to let repeated starts rebuild or relaunch partial runtime state after users thought the runtime had stopped.

This owner captures the first implementation slice that closes that seam without reopening broader runtime architecture work: reject repeated user sta

canonical: docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md
