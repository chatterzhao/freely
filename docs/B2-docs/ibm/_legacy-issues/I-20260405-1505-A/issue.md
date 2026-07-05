---
local_id: I-20260405-1505-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '109'
    url: https://github.com/chatterzhao/freely/issues/109
    synced_at: '2026-04-27T11:24:33Z'
  gitee:
    issue_id: IJFO8P
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8P
    synced_at: '2026-04-27T13:16:27Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:33Z'
hash: ''
created_at: '2026-04-27T11:24:33Z'
updated_at: '2026-05-17T12:22:56Z'
platform_state: closed
---

The read-only semantic-loop signal introduced under `I-20260322-0445` is supposed to stay conservative: it should surface only when the manager keeps rewriting equivalent continuity while no worker is actually running and capacity is still available. Current canonical `develop` still fails that contract. The same regression test proves the signal can remain active even after a worker supervisor and AI process are already present, which turns a monitoring hint into a false positive during normal 

canonical: docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md
