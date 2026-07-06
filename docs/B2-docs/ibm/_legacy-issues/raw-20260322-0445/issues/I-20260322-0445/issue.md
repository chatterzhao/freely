---
local_id: I-20260322-0445
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260322-0445/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '49'
    url: https://github.com/chatterzhao/freely/issues/49
    synced_at: '2026-04-27T11:16:47Z'
  gitee:
    issue_id: IJFO6H
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6H
    synced_at: '2026-04-27T13:14:49Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:47Z'
hash: ''
created_at: '2026-04-27T11:16:47Z'
updated_at: '2026-04-27T11:16:47Z'
platform_state: closed
---

The read-only semantic-loop signal introduced under `I-20260322-0445` is supposed to stay conservative: it should surface only when the manager keeps rewriting equivalent continuity while no worker is actually running and capacity is still available. Current canonical `develop` still fails that contract. The same regression test proves the signal can remain active even after a worker supervisor and AI process are already present, which turns a monitoring hint into a false positive during normal 

canonical: docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md
