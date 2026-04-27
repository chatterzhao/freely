---
local_id: I-20260406-1105-A
kind: linked
status: completed
platform_ids:
  github:
    issue_id: "120"
    url: "https://github.com/chatterzhao/freely/issues/120"
    synced_at: "2026-04-27T11:25:43Z"
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md"
last_synced_comment_at:
  github: "2026-04-27T11:25:43Z"
hash: ""
created_at: "2026-04-27T11:25:43Z"
updated_at: "2026-04-27T11:25:43Z"
---

The active milestone still keeps several completed owners in `committed_issues`. That conflicts with milestone policy and leaves the main orchestration surface with stale sequencing truth.

`governance-merge-gate` is not the missing contract here, because it only evaluates the current develop-bound diff. The missing contract is a baseline repo-wide audit that can detect historical queue drift already present on canonical `develop`.

canonical: docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md
