---
local_id: I-20260620T104526Z-A
kind: fix
phase_state: completed
milestone: ""
parent_raw: raw-20260620T104526Z
title: "fix: A2A SSE supervision — store worker session_id, enable session/prompt intervention"
created_at: "2026-06-20T11:10:00Z"
author: manager
implemented_in:
  branch: feature/raw-20260620T104526Z-worker-sse-supervision
  commits: []
---

## What

Store worker's ACP session_id in A2A task metadata after launch, enabling
Manager to use SSE streaming for real-time supervision and session/prompt for
active intervention.

## Changes

- **a2a_server.py**: Add `session_id` to POST /tasks and PATCH /tasks/{id} handlers
- **a2a_task.py**: Fix `process_ai_reply` signature (add missing `worktree` param),
  pass `session_id` to `c.create()`, add `--session-id` to update, add `prompt` command
- **freely**: Add `capture_worker_session_id_and_store()` to read worker session
  from cycle log and update A2A task; pass task_id through launch function;
  save `_a2a_task_id` before insert overwrites it; update A2A state to working
- **manager-agent.md**: Add SSE supervision + session/prompt intervention to
  patrol step 3; add get/update/prompt/SSE curl commands to command table
