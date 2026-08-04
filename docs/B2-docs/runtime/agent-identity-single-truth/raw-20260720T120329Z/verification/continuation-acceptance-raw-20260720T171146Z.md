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
| CAT-007 | wire codec 对称：裸预占、含冒号 session、多 reviewer 完整 pair 不串线 | `tests/test_agent_working_fail_closed_and_idempotent.py` | GREEN |
| CAT-008 | 重启恢复调用可执行模块路径，跳过裸预占并恢复每个精确 agent/session pair | same | GREEN |
| CAT-009 | watchdog/lifecycle/pr-review 生产读取入口统一使用 codec / session connector | focused + lifecycle suite | GREEN |

## Commands and actual results

```bash
python3 -m pytest \
  tests/test_regression_agent_id_env_gate.py \
  tests/test_agent_working_fail_closed_and_idempotent.py \
  tests/test_e2e_agent_working_socket.py \
  tests/test_agent_table_query_next_free.py \
  tests/test_e2e_agent_working_real_db.py \
  tests/test_agent_working_logic.py \
  tests/test_worker_launch_fail_closed_review.py -q
# actual: 53 passed in 0.55s

python3 -m pytest \
  tests/test_agent_working_logic.py \
  tests/test_e2e_agent_working_real_db.py \
  tests/test_watchdog_sse.py \
  tests/test_integration_lifecycle.py -q
# actual: 58 passed in 0.14s

python3 -m pytest tests/test_regression_agent_id_env_gate.py -q
# actual: 1 passed in 0.03s

python3 -m pytest tests/test_e2e_agent_working_real_db.py -q
# actual: 4 passed in 0.03s

python3 -m pytest \
  tests/test_agent_working_fail_closed_and_idempotent.py \
  tests/test_watchdog_sse.py \
  tests/test_integration_lifecycle.py -q
# final actual: 70 passed in 0.13s

python3 -m pytest tests -q --junitxml=/tmp/freely-agent-working-tests.xml
# actual: 124 passed in 0.78s; junit: failures=0, errors=0, skipped=0

python3 -m pytest -q
# actual: collection interrupted with 2 pre-existing errors:
# - docs/B2-docs/ibm/_legacy/raw-MIGRATED-sse-full-implementation/verification/test_sse_phase1.py
#   cannot import a2a_task
# - docs/system/workspace/scripts/runtime/a2a/test_a2a.py:203
#   historical SyntaxError: '[' was never closed
# Neither asset is modified by this continuation or included in its canonical tests/ suite.

bash -n bin/pr-review-guarded
python3 -m py_compile \
  docs/system/workspace/scripts/runtime/agent_identity_value.py \
  docs/system/workspace/scripts/runtime/agent_session_restore.py \
  docs/system/workspace/scripts/runtime/task-lifecycle-scan.py \
  docs/system/workspace/scripts/runtime/a2a/a2a_server.py \
  docs/system/workspace/scripts/runtime/watchdog_sse.py \
  docs/system/workspace/scripts/runtime/freely_db_manager.py
# actual: exit 0
```

## Governance status

- `./bin/freely live-status --project <continuation-worktree>` and `baseline-status` fail closed because the continuation worktree has no `agent_working` registration. This is expected identity enforcement, not a codec regression.
- `./bin/freely fleet-status --project <continuation-worktree>` is the identity-independent governance fallback and succeeds; it reports this worktree as `DIRTY` with `checkpoint=true`.
- `./bin/freely checkpoint-guard` succeeds and reports `checkpoint_required=yes`, `changed_files=15`, `untracked_files=2`, `reason_codes=scope_count_threshold`.
- `./bin/freely governance-check` reaches the repository gate but reports five pre-existing repository governance defects: missing `protected-branch-breakglass-receipts.md`, missing `docs/B1-docs/{README.md,INDEX.md,CONVERGENCE.md}`, and legacy `raw-20260303T000000Z` naming mismatch. None is introduced or modified by this continuation.

## Baseline (pre-fix)

13/13 old tests passed while production defects remained (false green).
