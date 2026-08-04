---
local_id: raw-20260724T024118Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '4071'
    url: https://github.com/chatterzhao/freely/issues/4071
    synced_at: ''
  gitee:
    issue_id: IK3P7O
    url: https://gitee.com/zhaoquan/freely/issues/IK3P7O
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-24T02:41:40Z'
updated_at: '2026-07-24T02:41:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
Historical evidence shows I-20260408-1205-A completed the verification handoff contract and explicitly deferred raw-command bypass and wrapper adoption to a follow-on. The repository has wrapper commands and verification metadata, but their lifecycle boundary is not stated as one auditable contract.

## 影响
Metadata can be created at intake, propagated through wrappers, or written as evidence without a clear owner, phase, freshness rule, or rejection condition. This makes B1/B2 routing and RED/GREEN evidence ambiguous and risks accepting stale or ownerless command results.

## 修复方案
Define and materialize a narrow command-wrapper metadata lifecycle: intake creation, guarded-wrapper propagation, issue-bound persistence, stale/ownerless rejection, and explicit B1/B2 plus RED/GREEN evidence. Keep scope to command-wrapper boundary and focused regressions; exclude completed verification-contract rewrites and broad runtime supervision changes.
