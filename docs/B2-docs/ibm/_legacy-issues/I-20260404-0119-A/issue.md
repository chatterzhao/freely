---
local_id: I-20260404-0119-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '97'
    url: https://github.com/chatterzhao/freely/issues/97
    synced_at: '2026-04-27T11:23:27Z'
  gitee:
    issue_id: IJFO8A
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8A
    synced_at: '2026-04-27T13:16:07Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:27Z'
hash: ''
created_at: '2026-04-27T11:23:27Z'
updated_at: '2026-06-21T15:21:45Z'
platform_state: closed
---

The active milestone still keeps several completed owners in `committed_issues`. That conflicts with milestone policy and leaves the main orchestration surface with stale sequencing truth.

`governance-merge-gate` is not the missing contract here, because it only evaluates the current develop-bound diff. The missing contract is a baseline repo-wide audit that can detect historical queue drift already present on canonical `develop`.

canonical: docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md
