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

## Independent review closure

- Six dimensions reviewed: architecture/data flow, fail-closed behavior, raw_key consistency, concurrency/idempotency, real socket coverage, governance/regression gates.
- First review verdict: blocked by scan RPC failure being misclassified as `never_bound`; manager registration and daemon canonicalization also had soft-failure paths.
- Resolution: all findings above fixed; continuation suite `37/37` GREEN; Python and Shell syntax checks GREEN; edited-file diagnostics contain no new findings.
- Repository-wide `pytest tests` still has two pre-existing collection errors for removed `watchdog_sse` private symbols; they are outside this continuation and not introduced by these changes.

## Non-goals

- No new I/C/M nodes
- No rewrite of historical pre-tests PASS evidence
- No commit / PR / merge from this worker
