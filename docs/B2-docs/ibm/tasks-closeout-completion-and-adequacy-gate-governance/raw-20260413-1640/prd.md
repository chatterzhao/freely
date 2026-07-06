# PRD: tasks-closeout-completion-and-adequacy-gate-governance

## Objective

Make owner completion and guarded adequacy fail closed when execution closeout in `tasks.md` is missing or still incomplete, while preserving `pre-tests.md` as the canonical verification truth.

## Product Requirements

1. `pretests-gate` must derive one owner-bound `tasks.md` alongside the bound `pre-tests.md`.
2. Completion checks must reject owners whose `tasks.md` is missing or still has unchecked task boxes.
3. `--require-adequacy` must apply the same `tasks.md` closeout gate before returning a pass verdict.
4. `governance-merge-gate` must inherit the new behavior by delegation only.
5. Focused regressions must cover both direct gate enforcement and inherited develop-merge behavior.

## Non-Requirements

1. No new verification ledger beside `pre-tests.md`.
2. No global repo-wide tasks audit in this owner.
3. No merge-gate-local `tasks.md` parser.
4. No redesign of task syntax beyond detecting the existing unchecked checkbox shapes.

## Non-Negotiables

- `pre-tests.md` remains the only canonical verification truth.
- `tasks.md` participates only as execution closeout completeness for the bound owner.
- missing `tasks.md` must fail closed during completion and adequacy paths rather than silently degrading.
- develop-bound merge behavior must stay aligned through `pretests-gate` delegation, not duplicated policy.

## Product Surface

- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Decomposition

1. Bind `tasks.md` path derivation to the owner contract.
2. Add missing-file and unchecked-task blockers to completion and adequacy verdicts.
3. Update direct gate regressions.
4. Keep delegated merge-gate coverage aligned.
5. Record lawful lifecycle evidence for the bounded repair.

## Eval Plan

Success:

- completed owners cannot pass with unchecked tasks
- guarded adequacy cannot pass with unchecked tasks
- delegated develop-merge coverage still passes when owner `tasks.md` is complete
- no second parser or alternate truth path is added

Failure:

- completed owners still outrun unchecked task boxes
- `--require-adequacy` ignores `tasks.md` closeout drift
- merge delegation requires separate hand-maintained fixture logic because the owner contract is inconsistent

## Revisit Triggers

- if future issue governance requires a broader closeout ledger than owner `tasks.md`
- if repo-wide completed-state audits need to become a separate watchdog owner instead of living as focused gate enforcement
