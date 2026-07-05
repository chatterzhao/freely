---
candidate_id: C-20260625T211802Z-A
status: promoted
source_raw: raw-20260625T211813Z02Z
created_at: 2026-06-26
milestone: M-20260625T211802Z-A
---

## C-20260625T211802Z-A: legacy issue

- candidate_format_version: v2
- title: agent-table slot 全链路
- status: promoted
- next_action: implement
- acceptance_criteria:
  - agent-table-query --next-free: scan worktrees, detect busy workers
  - sync_tooling: write worker-id.env with assigned worker_id
  - pr-review-guarded: read reviewer_slot from agent-table
  - Manager: read manager_slot
  - manager_max_parallel_workers: use pool count
- promoted_issue_path: docs/issues/I-20260625T211802Z-A/issue.md
- milestone: M-20260625T211802Z-A
- session_refs: []
