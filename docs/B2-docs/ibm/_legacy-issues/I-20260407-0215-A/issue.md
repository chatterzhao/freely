---
local_id: I-20260407-0215-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '124'
    url: https://github.com/chatterzhao/freely/issues/124
    synced_at: '2026-04-27T11:26:02Z'
  gitee:
    issue_id: IJFO99
    url: https://gitee.com/zhaoquan/freely/issues/IJFO99
    synced_at: '2026-04-27T13:16:48Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:26:02Z'
hash: ''
created_at: '2026-04-27T11:26:02Z'
updated_at: '2026-05-17T12:23:32Z'
platform_state: closed
---

This owner was opened because canonical root `develop` showed a narrow but reusable self-host supervision gap:

1. the latest manager prompt explicitly requires a new continuity file
2. the latest generated continuity is still older than that prompt
3. delegated continuation evidence remains pending
4. status previously could degrade all the way to blank output when PID hint validation failed under `set -e`

This is not a CLI-first owner and not a generic watchdog redesign. It is the next bounde

canonical: docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md
