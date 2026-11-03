---
schema_version: '1'
local_id: raw-20260807T121205Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4109'
    url: https://github.com/chatterzhao/freely/issues/4109
    synced_at: ''
  gitee:
    issue_id: IK78A5
    url: https://gitee.com/zhaoquan/freely/issues/IK78A5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T12:12:05Z'
updated_at: '2026-08-07T12:12:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

## Symptom
Workers request phase reviews via a2a-exit --state input-required --reason needs-review:<phase>, but NO reviewer is ever spawned. watchdog_sse.log shows repeated:
    [watchdog] input-required: reason=needs-review:b1 needs_role=reviewer
    [watchdog] FAIL-CLOSED: missing raw_key for reviewer assign
Reviewer pool stays busy=0. Workers proceed through phases WITHOUT review approval (observed worker_08 going b1->b2->red->dev->test), so the phase-review governance gate is silently bypassed.

## Root cause
watchdog_sse.py _handle_needs_reviewer reads raw_key from the SSE event metadata:
    raw_key = _normalize_raw_key(metadata.get('raw_key', ''))
    ...
    if not rid:
        if not raw_key: FAIL-CLOSED

The SSE state_update event is built in a2a/a2a_server.py PATCH /tasks/{id} handler:
    _notify_sse(task_id, 'state_update', { 'task_id':..., 'state':..., **fields })
where fields only contains what the PATCH body sent. The a2a-exit UPDATE path in a2a_task.py (existing_task_id branch) sends only state/summary/next/evidence/reason — it does NOT include raw_key:
    r = c.update(existing_task_id, state=state, summary=..., next=..., evidence=..., reason=reason)
So the SSE event never carries raw_key -> reviewer assign always FAIL-CLOSED.

## Impact
- Phase reviews (B1/B2/RED/dev/test) never happen -> governance gap, unreviewed work can reach PR/merge.
- Workers may wait indefinitely at review gates OR proceed unreviewed (observed: proceed).

## Expected fix (pick one)
1. a2a_task.py a2a-exit update path: include raw_key (from args or task record) in the update call so the SSE event carries it.
2. watchdog_sse.py _handle_needs_reviewer: when metadata raw_key is empty, look up raw_key from the task record (a2a_task.get) using metadata task_id, before FAIL-CLOSED.
3. a2a_server.py PATCH handler: enrich the state_update SSE event with the task's stored raw_key from the task store.

## Evidence
- .freely/run/watchdog-sse.log FAIL-CLOSED entries 11:57-12:09Z
- worker tasks: cabd8c06 (scan), 11e61147 (chat) — input-required needs-review recorded but reviewer never assigned
- a2a_task.py a2a-exit update branch (L1104-1110) missing raw_key
