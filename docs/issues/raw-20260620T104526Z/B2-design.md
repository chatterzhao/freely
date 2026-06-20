# B2: Design — A2A SSE Supervision + Worker Session Tracking

## Architecture

### Session ID Pass-Through Chain

```
run-acp-prompt.py (stdout line 1 = session UUID)
    ↓
capture_worker_session_id_and_store() [freely runtime]
    ↓ reads first line of cycle-worker-*.log
a2a_task.py update --task-id X --session-id Y
    ↓ PATCH /tasks/{task_id} {"session_id": "Y"}
A2A Server _task_endpoint PATCH handler
    ↓ fields["session_id"] → update_fields()
SQLiteTaskStore → freely_db_manager.h_a2a_task_update()
    ↓ UPDATE a2a_tasks SET session_id = ?
DB column a2a_tasks.session_id TEXT
```

### Changes

#### 1. a2a_server.py — session_id in REST handlers

**POST /tasks** (`_tasks_endpoint`):
Add `"session_id": body.get("session_id", "")` to fields dict.
This allows `session_id` to be stored at task creation time.

**PATCH /tasks/{task_id}** (`_task_endpoint`):
Add `"session_id"` to the field extraction loop.
This allows `session_id` to be updated after worker launch.

#### 2. a2a_task.py — session_id in process_ai_reply

Fix `process_ai_reply` signature: add missing `worktree` parameter (pre-existing bug).
Add `session_id` to `c.create()` call, passing it through to A2A Server.

Add `--session-id` argument to `update` subcommand.
Add `prompt` subcommand (--task-id, --message) for session/prompt intervention.

#### 3. freely runtime — session capture

New function `capture_worker_session_id_and_store()`:
- Runs in background subprocess
- Polls worker cycle log for first line (session UUID)
- Validates UUID format via regex
- 30s timeout, 1s polling interval
- Calls `a2a_task.py update --task-id X --session-id Y`

`launch_worker_from_manager_prompt_if_needed()`:
- Accepts optional 4th parameter `task_id`
- Calls `capture_worker_session_id_and_store` from both bridge and agent-fallback paths

`consume_delegate_workers` loop:
- Saves original `_a2a_task_id` before insert overwrites `_task_id`
- Passes `_a2a_task_id` to launch function
- Updates A2A task state to "working" after successful launch

#### 4. manager-agent.md — SSE + intervention instructions

Step 3 renamed to "检查 Worker 容量与 SSE 监督".
Added subsections:
- Worker 实时监督（SSE 流式订阅）: session_id check, SSE subscription, stall detection
- session/prompt 干预机制: when and how to intervene

Commands table: added `get`, `update`, `prompt`, and SSE curl command.

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Session capture fails (slow ACP) | 30s timeout, log warning, next patrol retries |
| UUID validation false negative | Regex supports both dashed and undashed UUIDs |
| worktree param was missing in process_ai_reply | Added; caller already passed it, now function accepts it |
| `_a2a_task_id` not set for non-consumer callers | `task_id="${4:-}"` defaults to empty; capture short-circuits |
| Background subprocess leaks | Exits after timeout or success; no infinite loop |
