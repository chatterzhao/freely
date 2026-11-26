---
schema_version: '1'
local_id: raw-20260807T121205Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T121205Z-A
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
canonical_issue_path: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/issues/I-20260807T121205Z-A.md
last_synced_comment_at:
  github: '2026-11-26T10:00:00Z'
  gitee: '2026-11-26T10:00:00Z'
hash: ''
created_at: '2026-08-07T12:12:05Z'
updated_at: '2026-11-26T10:46:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20260807T121205Z-A
source_candidate: ''
completed_at: '2026-11-26T09:59:59Z'
closeout_note: ''
---

# fix: reviewer assign FAIL-CLOSED missing raw_key in SSE event

workflow_kind: fix

## fix: reviewer assign FAIL-CLOSED missing raw_key in SSE event

| Field | Value |
|-------|-------|
| local_id | `raw-20260807T121205Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/issues/I-20260807T121205Z-A.md` |
| created | 2026-08-07T12:12:05Z |
| updated | 2026-08-07T12:12:30Z |

---

> **Freely 治理**：这是 raw issue `raw-20260807T121205Z`。实现前请用 `wt-create --raw-key 20260807T121205Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

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

### comment-20261126T100000Z
- source: system
- event: promote_finalized
- children: ["I-20260807T121205Z-A"]

拆解为以下任务:
1. [I-20260807T121205Z-A](will-be-updated)
