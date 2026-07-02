# Pre-Tests: A2A Reviewer Agent — ACP/A2A/SSE/Session 集成
- issue_id: I-20260701T085407Z-A

## Acceptance Items

### AT-001: agent_working table CRUD logic
- **Given**: agent_working SQLite table with raw_key PK, manager_id/worker_id/reviewer_id columns
- **When**: agent_assign(upsert), agent_assign(update_only), agent_get_session, agent_next_free called
- **Then**: pair parse/format roundtrips correctly, reviewer_id appends not overwrites, __manager__ key works
- **Verify**: `python3 -m pytest tests/test_agent_working_logic.py -v`
- **Status**: passed (8 tests, 0.07s)

### AT-002: InputRequiredReason 12-value enum
- **Given**: InputRequiredReason enum with 12 values + UNKNOWN fallback
- **When**: from_string() parses reason strings, needs_role property routes to manager/worker/reviewer
- **Then**: all 12 values route correctly, UNKNOWN falls to manager, 6 bidirectional routes covered
- **Verify**: `python3 -m pytest tests/test_input_required_reason.py -v`
- **Status**: passed (7 tests, 0.07s)

### AT-003: _restore_tasks and/or priority fix
- **Given**: a2a_server.py _restore_tasks with L403/442/663 and/or precedence bugs
- **When**: restore logic runs with mixed worker+reviewer states
- **Then**: parentheses correctly group conditions, no false routing
- **Verify**: `python3 -m pytest tests/test_restore_tasks_priority.py -v`
- **Status**: passed (4 tests, 0.07s)

### AT-004: watchdog SSE parsing + ACP RPC + handler routing
- **Given**: watchdog_sse.py subscribed to A2A SSE global stream
- **When**: SSE events arrive with flat format {state, reason, from_agent, needs_role, raw_key}
- **Then**: _handle_sse_event parses correctly, routes by needs_role to _handle_needs_reviewer/worker/manager
- **When**: _handle_needs_reviewer dispatches Reviewer via session/fork from Manager or session/new
- **Then**: _acp_session_fork uses __manager__ key, _create_reviewer_session calls update_only agent_assign
- **Verify**: `python3 -m pytest tests/test_watchdog_sse.py -v`
- **Status**: passed (19 tests, 0.07s)

### AT-005: lifecycle integration D8-D13
- **Given**: multi-agent system with Manager/Worker/Reviewer sessions
- **When**: freely restart (D8), agent crash (D9), active session (D10), dead session (D11), three-loop (D12), E2E (D13)
- **Then**: sessions survive/persist correctly, agents resume from agent_working, SSE events route properly
- **Verify**: `python3 -m pytest tests/test_integration_lifecycle.py -v`
- **Status**: passed (26 tests, 0.09s)

### AT-006: full test suite regression
- **Given**: all 6 test files covering agent_working, InputRequiredReason, _restore_tasks, watchdog, lifecycle, a2a_tasks
- **When**: full pytest suite runs
- **Then**: all 82 tests pass with no failures
- **Verify**: `python3 -m pytest tests/ -v`
- **Status**: passed (82 tests, 0.10s)

### AT-007: governance gate acceptance
- **Given**: I-* issue with completed phase_state, pre_tests_path, verification_artifact_dir, Implementation Decision Note
- **When**: pr-create-guarded runs IBM governance gate
- **Then**: gate passes (all review docs reference I-20260701T085407Z-A, candidate absorbed with correct path)
- **Status**: passed (governance gate PASS with warnings only)

## Test Lane

- `feature-local`: AT-001 through AT-007 runnable in fix and test-pre-merge worktrees
- `premerge-integration`: AT-006 (full pytest) runs in test-pre-merge before pr-create
