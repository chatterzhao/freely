# PRD: stale-prebrainstorm-truth-reconcile-governance

## Objective

Establish a narrow reconcile policy for pre-brainstorms whose statements are stale, superseded, or deferred, so audits consume canonical truth instead of outdated text.

## Product Requirements

1. Define a strict triage model for stale/superseded/deferred with deterministic precedence.
2. Require each reconcile edit to include canonical truth pointers (owner issue/PRD/pre-tests and, when applicable, executable gate/hook/test truth).
3. Limit first materialization to a representative batch only; no repository-wide cleanup.
4. Preserve deferred intent by marking it as deferred with owner pointer, not by deleting it.
5. Preserve `pre-tests.md` as the single evolving success-standard/test-task artifact name; do not introduce `tests.md`.
6. Keep this owner documentation-only and policy-only; runtime/gate behavior changes are out of scope.

## Representative Batch For First Materialization

1. Superseded-by-implementation sample:
   - `docs/B1-docs/raw-20260408-1205/brainstorms.md`
2. Absorbed-and-closed sample:
   - `docs/B1-docs/raw-20260406-0055/brainstorms.md`
3. Deferred-by-owner-boundary sample:
   - `docs/B1-docs/raw-20260327-0651/brainstorms.md`
4. Split-and-partially-materialized sample:
   - `docs/B1-docs/raw-20260405-1615/brainstorms.md`

## Non-Requirements

1. No runtime, hook, or quality gate logic modifications.
2. No auto-scan or auto-rewrite system for all historical pre-brainstorms.
3. No broad `docs/B1-docs/raw-INDEX.md` rewrite in the first batch; only minimal owner-registration append is allowed when required by standard materialization.
4. No bundling of launch-time hard-gate owner work into this owner.
