# Verification: tasks-closeout-completion-and-adequacy-gate-governance

- issue_id: `I-20260413-1640-A`
- issue_path: `docs/epics/workspace-routing-foundation/tasks-closeout-completion-and-adequacy-gate-governance/issues/tasks-closeout-completion-and-adequacy-gate-governance.md`
- verification_date: `2026-04-13`
- verifier: `codex`

## Scope Verdict

- `PASS`: `pretests-gate` now derives one owner-bound `tasks.md` path, honoring explicit `tasks_path` when present and defaulting to the sibling tasks ledger otherwise.
- `PASS`: completed owners now fail closed when `tasks.md` is missing or still contains unchecked task boxes, closing the drift exposed by `I-20260413-0420-B` and `I-20260413-0420-C`.
- `PASS`: guarded adequacy now applies the same tasks closeout blocker before returning an owner-bound pass verdict.
- `PASS`: delegated `governance-merge-gate` coverage stays aligned through `pretests-gate` without introducing a second `tasks.md` parser.
- `PASS`: focused regression coverage proves the owner remains narrow: `pre-tests.md` still owns verification truth, while `tasks.md` only gates execution closeout completeness.

## Commands

1. `bash -n docs/system/workspace/scripts/quality/pretests-gate`
2. `bash docs/system/workspace/scripts/tests/test-pretests-gate`
3. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
4. `./bin/governance-check`
5. `git diff --check`

## Implementation Decision Note

- decision: `Bind sibling tasks closeout truth into pretests-gate for completion and guarded adequacy instead of widening governance-merge-gate into a second closeout parser.`
- why_this: `pretests-gate already owns owner-level completion and adequacy decisions, so adding tasks closeout there closes the real contract gap while keeping verification truth and merge delegation aligned.`
- alternatives_considered: `Parse tasks.md directly in governance-merge-gate; add a new tests ledger beside pre-tests and tasks; leave the gap to repo-wide audit only.`
- boundary_non_goals: `This owner does not demote pre-tests.md, does not add a new merge-only parser, and does not widen into generic issue-document linting.`
- residual_risk: `Historical completed owners that already drifted before this gate landed still require manual document reconciliation; future follow-ons may add repo-wide watchdog auditing if passive drift detection proves necessary.`
