# Continuation Acceptance — raw-20260720T171146Z

- parent_story: M-20260720T120329Z-A / I-20260720T120329Z-A,B,C
- absorbed_raw: raw-20260720T171146Z
- phase: verification continuation (no new I/C/M nodes)

## Historical false-green note

Parent AT-001 / AT-002 in `pre-tests.md` previously marked GREEN, but:

1. Regression gate only scanned `scripts/` with loose string allowlists and skipped `bin/`.
2. E2E called `daemon.dispatch` directly — not a real AF_UNIX client/server path.
3. Production still had `manager_01`/`worker_01` silent fallbacks and `agent-id.env` reads in bin.

Those PASS rows are **historical evidence of incomplete coverage**, not proof of residual closure.
Do not rewrite those PASS markers; this file is the continuation truth.

## Continuation acceptance

| id | requirement | test | status |
|----|-------------|------|--------|
| CAT-001 | fail-closed RPC + no silent manager/worker fallback | `tests/test_agent_working_fail_closed_and_idempotent.py` | GREEN |
| CAT-002 | next_free_and_assign idempotent + occupied bare/session | same | GREEN |
| CAT-003 | raw_key canon across assign/scan/review/close | socket E2E + unit | GREEN |
| CAT-004 | real AF_UNIX socket E2E (manager→worker→reviewer→close, concurrent, idempotent, review persist, DB down) | `tests/test_e2e_agent_working_socket.py` | GREEN |
| CAT-005 | bin+runtime regression gate (comments only) | `tests/test_regression_agent_id_env_gate.py` | GREEN |
| CAT-006 | agent-table-query --next-free exit 0; pr-review-guarded parse order | `tests/test_agent_table_query_next_free.py` | GREEN |

## Commands

```bash
python3 -m pytest \
  tests/test_regression_agent_id_env_gate.py \
  tests/test_agent_working_fail_closed_and_idempotent.py \
  tests/test_e2e_agent_working_socket.py \
  tests/test_agent_table_query_next_free.py \
  tests/test_e2e_agent_working_real_db.py \
  tests/test_agent_working_logic.py \
  tests/test_worker_launch_fail_closed_review.py -v
# expected: 37 passed
```

## Baseline (pre-fix)

13/13 old tests passed while production defects remained (false green).
