---
local_id: I-20260619T035704Z-A
kind: linked
phase_state: in_verification
source_raw: raw-20260619T035704Z
source_candidate: docs/pre-brainstorms/20260619T035704Z--parse-candidate-heading-regex/candidates.md#C-20260619T035704Z-A
verification_artifact_dir: docs/epics/parse-candidate-heading-regex
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
