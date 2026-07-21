# Implementation Decision Note — raw-20260720T171146Z continuation

## Decisions

1. **Shared raw_key boundary** — new `raw_key_canon.py`; all agent_working client APIs and DB handlers canonicalize before read/write.
2. **Fail-closed RPC** — `_db_rpc` raises `AgentWorkingError` on connect/transport/JSON-RPC error/null result; no empty-dict success that looks like “no agent”.
3. **Idempotent assign** — `next_free_and_assign` returns existing agent for same raw_key+role without overwrite; occupied set parses both bare and `id:session` (including reviewer CSV).
4. **Launch uses atomic return** — freely worker launch and watchdog routes call `agent_next_free_and_assign` / `agent_next_free(..., raw_key=...)` and pick slot from returned id; removed `worker_01`/`manager_01` silent fallbacks on those paths.
5. **agent-id.env** — removed live reads from `pr-review-guarded`, `freely-review`, `agent-table-query` reconcile; gate scans `bin/` + `runtime/` with comment-only allow.
6. **Socket E2E** — dedicated test server over AF_UNIX; does not count as E2E if only `dispatch` is called (parent AT-002 remains historical/partial).
7. **Scan uncertainty is not absence** — agent_working lookup failures emit non-ready `3_binding_unavailable`; they never become `3a_never_bound` or re-delegation instructions.
8. **Registration/canonicalization stay fail-closed** — manager session registration propagates failure, and daemon-side raw_key normalization rejects invalid keys instead of writing them unchanged.
9. **Storage/read symmetry** — a reservation without a live session is stored as bare `agent_NN`; only established sessions use `agent_NN:session_id`. Reviewer CSV preserves mixed bare/session entries, exact-agent session lookup never borrows another reviewer’s session, and release handles both forms.

## Independent review closure

- Six dimensions reviewed: architecture/data flow, fail-closed behavior, raw_key consistency, concurrency/idempotency, real socket coverage, governance/regression gates.
- First review verdict: blocked by scan RPC failure being misclassified as `never_bound`; manager registration and daemon canonicalization also had soft-failure paths.
- Resolution: all findings above fixed; final protocol/lifecycle regression `70/70` GREEN and canonical `tests/` suite `124/124` GREEN; edited-file diagnostics contain no new findings.
- Unconstrained repository-wide `pytest -q` still has two pre-existing collection errors: legacy `test_sse_phase1.py` cannot import `a2a_task`, and historical `runtime/a2a/test_a2a.py:203` has an unclosed list literal. They are outside this continuation and not introduced by these changes.

## Non-goals

- No new I/C/M nodes
- No rewrite of historical pre-tests PASS evidence
- No push / PR / merge from this worker
