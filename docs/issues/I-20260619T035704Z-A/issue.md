---
local_id: I-20260619T035704Z-A
kind: linked
phase_state: in_dev
source_raw: raw-20260619T035704Z
source_candidate: C-20260619T035704Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: I-20260619T035704Z-A
last_synced_comment_at: {}
created_at: 2026-06-19
session_refs: []
---

## Fix: parse_candidate_file heading regex #{1,3} + diagnostic

Change `^##{1,3}` → `^#{1,3}` in governance-merge-gate line 417.

Also add diagnostic hint when candidate file exists but heading doesn't match.
