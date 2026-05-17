---
local_id: I-20260413-0420-D
kind: linked
phase_state: completed
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '147'
    url: https://github.com/chatterzhao/freely/issues/147
    synced_at: '2026-04-27T11:27:29Z'
  gitee:
    issue_id: IJFO9Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9Y
    synced_at: '2026-04-27T13:17:19Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:27:29Z'
hash: ''
created_at: '2026-04-27T11:27:29Z'
updated_at: '2026-05-17T08:02:17Z'
platform_state: closed
---

Canonical `develop` now has the two prerequisite truths for this lane:

1. startup authority/readiness is already authoritative, so launch truth no longer depends on PID or argv resemblance
2. the manager startup contract already froze `launch_bootstrapped` versus `manager_handoff_materialized`
3. the runtime already knows the prompt-required continuity path before AI launch
4. stop fallback already knows how to write a repair continuity file, but normal startup still does not write a first hand

canonical: docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md
