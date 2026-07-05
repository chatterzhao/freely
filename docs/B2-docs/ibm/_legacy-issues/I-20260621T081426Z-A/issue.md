---
local_id: I-20260621T081426Z-A
kind: linked
phase_state: completed
source_candidate: docs/B1-docs/raw-20260621T081426Z/candidates.md#C-20260621T081426Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/B1-docs/raw-20260621T081426Z/candidates.md
created_at: '2026-06-21T08:14:26Z'
author: claude
channel: claude
source_raw: raw-20260621T081426Z
candidate_id: C-20260621T081426Z-A
milestone_id: M-20260621T081426Z-A
---

# I-20260621T081426Z-A: complete intake migration

## Map
### PRD
1. Manager sees chat messages from freely.db
2. Handler supports docs/issues/ paths
3. Stale chat cleanup (7 day retention)

### Tasks
- [x] chat_intake_snapshot_for_project reads from freely.db
- [x] append_human_chat_intake_if_needed calls new function
- [x] interruption-manager-handler supports raw-*/I-* paths
- [x] stale consumed=1 → consumed=-1 after 7 days

### Code Review
- issue_id: I-20260621T081426Z-A
- reviewer: claude
- verdict: pass
