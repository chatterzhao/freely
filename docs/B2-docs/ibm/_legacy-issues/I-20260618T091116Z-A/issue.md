---
issue_id: I-20260618T091116Z-A
kind: fix
phase_state: completed
milestone: M-20260618T091116Z-A
source_candidate: docs/B1-docs/raw-20260618T091116Z-write-task-mode-ordering/candidates.md#C-20260618T091116Z-A
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260618T091116Z-A/issue.md
title: Fix write_task_mode ordering — ensure DB daemon running first
---

# I-20260618T091116Z-A: write_task_mode before ensure_freely_db ordering fix

- title: Fix write_task_mode ordering — ensure DB daemon running first
- source: `raw-20260618T091116Z` (GitHub #2985)
- milestone: M-20260618T091116Z-A
- source_candidate: `docs/B1-docs/raw-20260618T091116Z-write-task-mode-ordering/candidates.md#C-20260618T091116Z-A`
- issue_id: I-20260618T091116Z-A
- phase_state: completed
- component: runtime

## Branch

- feature branch: `fix/raw-20260618T091116Z-write-task-mode-after-ensure-db`
- implementation commit: (see git log)

## Deliverables

### B2_IBM
- PRD: `docs/epics/write-task-mode-ordering/prd.md`
- Pre-tests: `docs/epics/write-task-mode-ordering/pre-tests.md`
- Tasks: `docs/epics/write-task-mode-ordering/tasks.md`
- Code review: `docs/B2-docs/write-task-mode-ordering/code-reviews/review.md`

### Implementation
- `docs/system/workspace/scripts/runtime/freely` — Added ensure_freely_db before write_task_mode in cmd_start() and cmd_daemon_start()
