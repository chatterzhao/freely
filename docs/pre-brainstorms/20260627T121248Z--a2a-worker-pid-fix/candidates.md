---
candidate_id: C-20260627T121248Z-A
status: promoted
source_raw: raw-20260627T121248Z
created_at: 2026-06-27
milestone: M-20260627T121248Z-A
---

## C-20260627T121248Z-A: a2a worker_pid + manager check fix

- candidate_format_version: v2
- title: a2a worker_pid + manager check fix
- status: promoted
- decision_reason: WT2 missed insert-side and a2a_server manager check
- next_action: B2_IBM -> dev -> pr-merge
- acceptance_criteria:
  - freely insert passes --worker-pid
  - a2a_server uses startswith for manager
- promotion_gate: new task has worker_pid non-empty
- promoted_issue_path: docs/issues/I-20260627T121248Z-A/issue.md
- milestone: M-20260627T121248Z-A
