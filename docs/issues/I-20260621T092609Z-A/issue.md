---
local_id: I-20260621T092609Z-A
kind: linked
phase_state: completed
source_candidate: docs/pre-brainstorms/20260621T092609Z--zombie-resume-on-restart/candidates.md#C-20260621T092609Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/pre-brainstorms/20260621T092609Z--zombie-resume-on-restart/candidates.md
created_at: '2026-06-21T09:26:09Z'
author: claude
channel: claude
source_raw: raw-20260621T092609Z
candidate_id: C-20260621T092609Z-A
milestone_id: M-20260621T092609Z-A
---

# I-20260621T092609Z-A: stop-side worker state preservation

## Map
### PRD
Before A2A server shutdown in stop_project_runtime, transition all working worker tasks to input-required so they can be resumed on next start.

### Tasks
- [x] Add worker state transition loop before A2A server stop (L20117)

### Code Review
- issue_id: I-20260621T092609Z-A
- reviewer: claude
- verdict: pass
