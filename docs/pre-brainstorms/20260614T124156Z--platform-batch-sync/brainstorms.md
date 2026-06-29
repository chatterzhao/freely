---
name: platform-batch-sync
raw_key: raw-20260614T124156Z
created: 2026-06-14T12:42:00Z
status: proposed
---

# Platform Batch Sync — Brainstorm

## Problem

Scan discovered an unsynced backlog:
- `pull=0 push=371 reconcile=0 close=66 platforms: github, gitee`

371 local issues need `issue-sync create/update` pushes to platforms.
66 platform issues need `issue-sync close` to mark local state as synced.

Last successful sync: `2026-06-13T10:53:11Z`.
Last scan: `2026-06-13T12:36:37Z`.

The batch sync was not automatically triggered after scan completed.

## Root Cause

`issue-sync batch` is a manual command — no runtime auto-trigger after scan.
Scan detects drift but doesn't execute the sync.

## Options

### A. Manual batch run
Run `freely issue-sync batch` directly.
Fastest, but requires human/agent action.

### B. Auto-sync after scan
Add `post-scan` hook to auto-trigger `issue-sync batch` when unsynced items > threshold.
Better DX, but adds runtime complexity.

### C. Health check + scheduled sync
Add `issue-sync health` subcommand + periodic cron/daemon check.
Most robust, but highest implementation cost.

## Recommendation

Start with A (manual batch to clear backlog).
Evaluate B as a follow-up if backlog recurs.

## Next
1. Run `freely issue-sync batch` on worktree
2. Verify sync results
3. Close platform issue #2667
