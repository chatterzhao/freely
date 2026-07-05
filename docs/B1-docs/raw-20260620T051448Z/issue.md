---
local_id: raw-20260620T051448Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T051448Z-A
platform_ids:
  github:
    issue_id: '3146'
    url: https://github.com/chatterzhao/freely/issues/3146
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T05:15:06Z'
updated_at: '2026-06-20T05:15:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

Manager patrol flow has no step to:
1. Query and consume completed worker tasks (handle closeout/merge)
2. Check active worker count before delegating new work
3. Exit with 'manager_working' when workers are running

Result: Manager blindly delegates all 76 scan items as worker tasks, never checks
if any workers finished, never stops delegating.

## Design

### New patrol flow (manager-agent.md)

Each patrol MUST execute in order:

1. **Pre-checks**: constitution + laws
2. **Consume completions**: query completed workers
   
   For each: read completion_summary → decide closeout/merge/followup

3. **Query running workers**:
   
   Count active workers. Prompt includes capacity info from Runtime.

4. **Decision gate**:
   - Active >= hard_cap(10)? → manager_working (wait, don't delegate)
   - Active >= soft_cap(7)? → delegate cautiously (max 2 new tasks)
   - Active < soft_cap? → delegate normally

5. **Delegate**: for each scan item, ensure worktree exists, then
   a2a-exit --state submitted --role worker

6. **Exit**: delegate_workers / manager_working / stop_ai

### Runtime prompt injection

Runtime injects into Manager prompt:
  active_workers: N
  worker_capacity: {soft: 7, hard: 10}
  worker_warning: "near capacity" | "at capacity" | null
