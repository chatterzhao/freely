---
local_id: I-20260420-1130-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '159'
    url: https://github.com/chatterzhao/freely/issues/159
    synced_at: '2026-04-27T11:28:37Z'
  gitee:
    issue_id: IJFOAD
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAD
    synced_at: '2026-04-27T13:17:39Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:37Z'
hash: ''
created_at: '2026-04-27T11:28:37Z'
updated_at: '2026-05-17T12:25:02Z'
platform_state: closed
---

Freely already has multiple places where a manager can discover work, but it still needed a runtime-owned answer to a narrower question: when should those surfaces be rescanned, and when should the current continuity or active worker remain authoritative?

The current self-host replay proved two opposite failures at the same seam:

1. stale delegated continuation could keep the manager from returning to higher-level task surfaces after startup or closeout
2. broad patrol could also pull the mana

canonical: docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md
