---
local_id: raw-20260620T104526Z26Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T104526Z-A
platform_ids:
  github:
    issue_id: '3159'
    url: https://github.com/chatterzhao/freely/issues/3159
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260620T104526Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T10:45:42Z'
updated_at: '2026-06-20T10:45:42Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

A2A Server has full SDK supervision infrastructure (SSE streaming, TaskStatusUpdateEvent,
subscriber registry, session/prompt mechanism) — but Manager never uses any of it.
Manager only polls DB via list --status completed during patrol.

Two missing pieces:
1. Worker session ID not stored in A2A task after launch → Manager can't use session/prompt
2. Manager patrol doesn't subscribe to SSE or check worker liveness

## Fix

### Store worker session ID
In launch_worker_from_manager_prompt_if_needed, after worker launches via run-acp-prompt.py,
capture the session ID and update the A2A task: a2a_task.py update --task-id X --session-id Y

### Manager SSE subscription
In patrol step 3 (check worker capacity), also:
- For each active worker, GET /tasks/{task_id}/stream to receive real-time status updates
- If no update from a worker for N minutes (stall timeout):
  - session/prompt to the worker session asking for status
  - If no response → mark worker as failed, let Manager decide next step

### Benefits
- Real-time awareness of worker progress (not just next patrol poll)
- Active intervention when workers stall (not silent failure)
- Uses already-implemented A2A SDK features (SSE, session/prompt)
