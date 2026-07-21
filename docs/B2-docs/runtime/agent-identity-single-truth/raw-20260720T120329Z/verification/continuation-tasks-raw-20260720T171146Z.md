# Continuation Tasks — raw-20260720T171146Z

1. [x] Baseline: run existing agent_working related tests (13 passed, false-green noted)
2. [x] RED: fail-closed / idempotent / raw_key / bin order tests
3. [x] Implement `raw_key_canon.py` + agent_working fail-closed RPC
4. [x] next_free_and_assign idempotent + occupied parse (bare + session)
5. [x] Production entrypoints: watchdog, freely launch, scan, pr-review-guarded, freely-review
6. [x] Remove live agent-id.env from bin + runtime; tighten regression gate
7. [x] Real AF_UNIX socket E2E
8. [x] Fix agent-table-query --next-free exit + --pool-size
9. [x] GREEN: continuation 验收集 53/53；watchdog/lifecycle 相关集 58/58；规范 `tests/` 全集 124/124；pre-tests 1/1 + 4/4；静态检查 exit 0
10. [x] Storage/read symmetry closure: codec 覆盖多 reviewer pair、裸预占、含冒号 session、restart restore、lifecycle scan、pr-review 入口
11. [x] Independent six-dimensional review completed; blocking implementation findings fixed
12. [x] Governance evidence recorded: identity-dependent status fail-closed without runtime registration; `fleet-status` fallback succeeds; repository-wide pytest/governance pre-existing blockers documented
13. [ ] Checkpoint commit / PR handoff blocked: governance exposes no Freely-wrapped commit command while this continuation forbids raw `git`; do not bypass
