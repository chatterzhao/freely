---
local_id: I-20260419-0333-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '154'
    url: https://github.com/chatterzhao/freely/issues/154
    synced_at: '2026-04-27T11:28:11Z'
  gitee:
    issue_id: IJFOA6
    url: https://gitee.com/zhaoquan/freely/issues/IJFOA6
    synced_at: '2026-04-27T13:17:32Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:11Z'
hash: ''
created_at: '2026-04-27T11:28:11Z'
updated_at: '2026-05-17T12:24:47Z'
platform_state: closed
---

The receipt-only closeout followthrough lane already proved that the main runtime lifecycle implementation had landed. But the preserved checkpoint on `feature/checkpoint-runtime-closeout-selfhost-validation-20260419` still carried real follow-on behavior that was not bound to any lawful owner:

1. `freely daemon start` should reuse a healthy same-project supervisor instead of launching a duplicate detached chain during closeout/self-host replay.
2. Ambiguous `project-start.lock` directories wit

canonical: docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md
