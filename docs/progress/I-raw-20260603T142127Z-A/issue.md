---
local_id: I-raw-20260603T142127Z-A
issue_id: I-raw-20260603T142127Z-A
issue_path: docs/issues/I-raw-20260603T142127Z-A/issue.md
---

## Implementation

- fix: issue-sync batch create linked I-* items (commit 8357a8b4)
- fix: scan cross-batch dedup via state file (commit 8357a8b4)
- chore: add raw issue lifecycle (commit 83067702)
- chore: add I-* governance issue (commit 2f960d67)

## Verification

- PR #2546 created
- All gates pass except final governance materialization (this commit)
