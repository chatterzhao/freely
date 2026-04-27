---
local_id: I-20260421-1530-A
kind: linked
status: completed
platform_ids:
  github:
    issue_id: "162"
    url: "https://github.com/chatterzhao/freely/issues/162"
    synced_at: "2026-04-27T11:28:50Z"
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/issues/live-status-scan-summary-and-prompt-anchor-governance.md"
last_synced_comment_at:
  github: "2026-04-27T11:28:50Z"
hash: ""
created_at: "2026-04-27T11:28:50Z"
updated_at: "2026-04-27T11:28:50Z"
---

Freely already had two valid but separate truths:

1. `task-source-scan` is the bounded patrol inventory contract
2. `live-status` is the current-state observation plane

What was still missing was a narrow implementation owner that applies the separation in runtime code without reducing capability:

1. prompt lookup on current-state hot paths must prefer explicit session anchors over prompt-history guessing
2. `live-status` should surface advisory patrol inventory from the existing scan JSON in

canonical: docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/issues/live-status-scan-summary-and-prompt-anchor-governance.md
