# Pre-tests — 20260430-0000--acp-session-store-and-lifecycle

Hotfix absorbed into chat-inbox-sqlite (I-20260429-2040-A). Tests executed:

## Test 1: session-store.py CLI round-trip
- `python3 session-store.py init --db /tmp/test-freely.db`
- `python3 session-store.py upsert --db ... --session-id $(uuidgen) --project /tmp/test --tool cc --launch-kind fresh --tool-adapter acp --role manager`
- `python3 session-store.py get-active --db ... --project /tmp/test --role manager` → returns clean UUID
- `python3 session-store.py complete --db ... --session-id <uuid> --status failed --error-reason auth_or_rate_limit`
- `python3 session-store.py get-active ...` → returns empty (failed sessions excluded)
- PASS

## Test 2: run-acp-prompt.py stdout format
- Verified all 5 code paths print `print(session_id)` as line 1 before annotated line 2
- PASS

## Test 3: monitor-ai-acp.sh session persistence
- `_persist_session_to_store` reads clean UUID from line 1, calls session-store.py upsert
- `_mark_session_failed` marks failed with error reason
- `_mark_session_completed` marks completed
- `_detect_acp_failure` now has 3 categories (auth, network, bridge_lost)
- PASS

## Test 4: select_launch_kind ACP mode
- No more cycle log text parsing
- No more `_find_recent_session_from_tool_dir` in ACP path
- Uses `session-store.py get-active` as authoritative source
- Falls back to in-memory CLAUDE_SESSION_ID_CURRENT if session-store unavailable
- PASS (code review)

## Test 5: Non-ACP regression guard
- `--bridge-lost-marker-file` only passed when adapter is `acp` (guarded by `_adapter_extra_args` array)
- `ensure_runtime_tool_session_anchor` keeps original `_find_recent_session_from_tool_dir` for non-ACP
- `extract_tool_session_id_from_log` ACP branch removed, codex branch kept
- PASS (code review)

## Test 6: freely.db rename
- All `chat-inbox.db` references renamed to `freely.db`
- `chat-inbox.py` and `session-store.py` both use the same DB
- `freely init` calls both `init` commands (idempotent via IF NOT EXISTS)
- PASS (code review)
