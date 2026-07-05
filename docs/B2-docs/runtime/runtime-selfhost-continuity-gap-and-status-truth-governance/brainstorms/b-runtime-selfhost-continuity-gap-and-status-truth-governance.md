# Brainstorm: runtime-selfhost-continuity-gap-and-status-truth-governance

## Decision

`C-20260407-0215-A` should promote into a dedicated self-host runtime followthrough owner.

## Why This

1. The blocked-supervision family already owns prompt-visible-but-unclaimed truth, but canonical `develop` now exposes a narrower recurrence: the prompt-required continuity path itself is missing.
2. The current active CLI help/dry-run owner explicitly leaves runtime supervision out of scope.
3. Status observability must degrade safely before any broader self-healing is trustworthy.

## Follow-on Package

The current implementation lane must consume:

1. `issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
2. `prd.md`
3. `pre-tests.md`
4. `tasks.md`
5. `docs/B1-docs/raw-20260407/brainstorms.md`
6. `docs/B2-docs/runtime/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`

## Boundary Summary

This owner freezes:

1. PID-hint failure as a degrade path instead of a blank status abort
2. `rg`-missing workspace-root fallback as a runtime capability requirement
3. prompt-required continuity gaps as an explicit status family

This owner does not freeze:

1. generic restart policy redesign
2. broad manager self-healing semantics
3. unrelated milestone/worktree cleanup drift

## Implementation Start Checklist

1. Keep the first slice bounded to status truth and degrade behavior already reproduced on canonical `develop`.
2. Verify every runtime code change with focused status regressions before widening into recovery behavior.
3. Do not claim that the continuity gap is healed automatically unless a later slice writes machine-readable recovery truth for it.
