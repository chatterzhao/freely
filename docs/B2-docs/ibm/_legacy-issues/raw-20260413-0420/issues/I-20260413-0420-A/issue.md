---
local_id: I-20260413-0420-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260413-0420/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '144'
    url: https://github.com/chatterzhao/freely/issues/144
    synced_at: '2026-04-27T11:27:13Z'
  gitee:
    issue_id: IJFO9V
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9V
    synced_at: '2026-04-27T13:17:14Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zissues/runtime-startup-authority-and-readiness-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:27:13Z'
hash: ''
created_at: '2026-04-27T11:27:13Z'
updated_at: '2026-05-17T08:02:02Z'
platform_state: closed
---

Canonical `develop` now has the two prerequisite truths for this lane:

1. startup authority/readiness is already authoritative, so launch truth no longer depends on PID or argv resemblance
2. the manager startup contract already froze `launch_bootstrapped` versus `manager_handoff_materialized`
3. the runtime already knows the prompt-required continuity path before AI launch
4. stop fallback already knows how to write a repair continuity file, but normal startup still does not write a first hand

canonical: docs/B2-docs/ibm/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md
