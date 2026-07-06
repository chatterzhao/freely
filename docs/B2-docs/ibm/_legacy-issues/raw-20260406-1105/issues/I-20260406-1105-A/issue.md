---
local_id: I-20260406-1105-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260406-1105/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '120'
    url: https://github.com/chatterzhao/freely/issues/120
    synced_at: '2026-04-27T11:25:43Z'
  gitee:
    issue_id: IJFO92
    url: https://gitee.com/zhaoquan/freely/issues/IJFO92
    synced_at: '2026-04-27T13:16:42Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:43Z'
hash: ''
created_at: '2026-04-27T11:25:43Z'
updated_at: '2026-05-17T12:23:20Z'
platform_state: closed
---

The active milestone still keeps several completed owners in `committed_issues`. That conflicts with milestone policy and leaves the main orchestration surface with stale sequencing truth.

`governance-merge-gate` is not the missing contract here, because it only evaluates the current develop-bound diff. The missing contract is a baseline repo-wide audit that can detect historical queue drift already present on canonical `develop`.

canonical: docs/B2-docs/ibm/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md
