# Continuation Tasks — raw-20260720T171146Z

1. [x] Baseline: run existing agent_working related tests (13 passed, false-green noted)
2. [x] RED: fail-closed / idempotent / raw_key / bin order tests
3. [x] Implement `raw_key_canon.py` + agent_working fail-closed RPC
4. [x] next_free_and_assign idempotent + occupied parse (bare + session)
5. [x] Production entrypoints: watchdog, freely launch, scan, pr-review-guarded, freely-review
6. [x] Remove live agent-id.env from bin + runtime; tighten regression gate
7. [x] Real AF_UNIX socket E2E
8. [x] Fix agent-table-query --next-free exit + --pool-size
9. [x] GREEN: 37/37 (continuation acceptance + fail-closed review regressions)
10. [x] Independent six-dimensional review completed; blocking findings fixed (PR remains pending owner commit authorization)
