---
local_id: raw-20260603T142127Z
kind: raw
phase_state: absorbed
title: fix-scan-cycling — issue-sync batch cannot push I-* linked items, causing platform_sync_batch
  to cycle infinitely
created_at: 2026-06-03 14:21:27+00:00
author: manager
session_refs: []
---

## Problem
The platform_sync_batch in the lifecycle scan keeps regenerating the same 423 items (push=356, close=67, reconcile=0) every scan run, even after workers have repeatedly run `issue-sync batch`. This wastes tokens and blocks Manager from making progress on real issues.

## Root Causes (from scan analysis)
1. `bin/issue-sync` cmd_batch() processes `linked` items (I-*) with cmd_update + cmd_close only — never cmd_create. The 59 I-* items without github.issue_id are permanently stuck as `local_only`.

2. `task-lifecycle-scan.py` add_platform_sync_batch() generates a new unique key each run (platform-sync-batch-{ts}), with no cross-scan dedup. Items already included in previous batches are re-included.

3. The batch next_action creates a new raw issue via `freely feedback`, which offsets any progress by adding itself back to the pool.

## Fix Required
1. Fix `bin/issue-sync` cmd_batch() to call cmd_create for linked items that lack github.issue_id, not just cmd_update.

2. Add cross-scan dedup in `task-lifecycle-scan.py` add_platform_sync_batch() to check `.scan-state` (or a marker in the batch item metadata) before re-including items.
