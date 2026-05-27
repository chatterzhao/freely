---
local_id: raw-20260527T004453Z
kind: raw
phase_state: absorbed
absorbed_into: "PR #2243 refactor: unified DB daemon"
platform_ids:
  github:
    issue_id: '2243'
    url: https://github.com/chatterzhao/freely/pull/2243
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-27 00:44:53+00:00
updated_at: 2026-05-27 00:44:53+00:00
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
---
## Problem

4 separate DB access paths competing for same freely.db:
- chat-inbox.py (chats table)
- session-store.py (sessions + tool_switch_events)
- handoff.py (handoffs table)
- Inline sqlite3 in freely bash (task_mode_gate)

Each spawns independent Python process with own SQLite connection. Results in:
- PRIMARY KEY collision (second-granularity timestamp ID)
- SQLite lock contention (OperationalError: database is locked)
- Inconsistent error handling (2>/dev/null everywhere)
- 30-50 Python cold starts per supervisor cycle

Previous unification (b7d031ae) only merged worker-store→handoff (schema level), didn't address connection level.

## Solution

freely_db_manager.py — single long-lived daemon owning one SQLite connection:
- Unix socket JSON-RPC (same pattern as acp-bridge.py)
- 40+ operations across all tables (chat/session/handoff/task-mode)
- Microsecond-precision chat IDs (no more collision)
- Structured error responses (no more 2>/dev/null)
- Thin CLI wrapper (freely-db-cli) for backward compat with old module args

## Scope

### Phase 1: Core daemon + CLI wrapper
- New: freely_db_manager.py (~600 lines)
- New: freely-db-cli (~200 lines Python thin client)
- New: handoff_parser.py (extracted from handoff.py, no DB)

### Phase 2: Replace inline sqlite3 + session-store in freely bash
- 6 inline sqlite3 blocks → freely-db-cli calls
- session-store CLI calls → freely-db-cli calls

### Phase 3: Replace calls in monitor-ai-acp.sh + stream-json-bridge.py

### Phase 4: Replace chat-inbox + handoff DB calls, remove old modules

## Expected Effect
- DB overhead per cycle: ~3-5s → ~150ms
- SQLite connections: 30-50 per cycle → 1 persistent
- PRIMARY KEY collisions: eliminated (single writer + microsecond IDs)
