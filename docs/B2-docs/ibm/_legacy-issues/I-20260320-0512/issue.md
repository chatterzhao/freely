---
local_id: I-20260320-0512
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '27'
    url: https://github.com/chatterzhao/freely/issues/27
    synced_at: '2026-04-27T11:14:26Z'
  gitee:
    issue_id: IJFO5M
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5M
    synced_at: '2026-04-27T13:14:18Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md
last_synced_comment_at:
  github: '2026-04-27T11:14:26Z'
hash: ''
created_at: '2026-04-27T11:14:26Z'
updated_at: '2026-04-27T11:14:26Z'
platform_state: closed
---

Freely 已经把 milestone 当成 standing source 和编排入口，但对 milestone sequencing、状态维护、写回 reconcile 的 owner 仍不清晰，导致 candidate/issue/progress/recovery/cleanup 之间的同步长期靠业务 worker 顺手维护。

本轮已经把 manager route、auto-loop、lifecycle 与专门 skill 全部补到位。现在需要把这条能力正式 materialize 成 canonical issue，让 milestone planning / state maintenance 成为 Freely 自己治理自身的一等能力。

canonical: docs/B2-docs/ibm/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md
