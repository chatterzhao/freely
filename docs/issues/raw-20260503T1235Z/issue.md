---
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
local_id: raw-20260503T1235Z
priority: P1
absorbed_into: I-20260503T1235Z-A
source: platform
updated_at: '2026-06-15T06:10:47Z'
platform_ids:
  github:
    issue_id: '186'
    owner: chatterzhao
    repo: freely
created_at: '2026-05-03T12:39:03Z'
title: 'fix: defer worker auto-recovery to after first AI patrol'
platform_state: closed
force_closed_at: '2026-06-13T11:23:09Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## Root Cause

Worker launch fails during daemon startup auto-recovery because infrastructure isn't ready yet.

### Timeline evidence
```
12:34:42 supervisor started
12:34:45 ACP bridge started
12:34:47 worker launch FAILED  ← auto-recover tried to launch worker!
12:34:47 target= (empty)       ← worktree cache not populated yet
```

### Failure chain
daemon start → auto-recover previous exit_contract workers → materialize_worker_prompt_worktree → fleet cache empty → returns empty target → worker launch fails → process churn → restart storm

### Fix
Defer manager_runtime_launch_workers_from_latest_handoff to after the first AI patrol cycle completes. Auto-recovery should happen in the manager_exit_contract_delegate_workers handler, AFTER the AI has run at least one patrol cycle.

### Also
Add diagnostic logging to all silent return 1 points in launch_worker_from_manager_prompt_if_needed.

### Status
Root cause confirmed. Fix identified. Issue CLOSED on GitHub.
