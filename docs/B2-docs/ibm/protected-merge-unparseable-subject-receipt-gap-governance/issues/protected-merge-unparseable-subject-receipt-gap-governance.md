# Issue: protected-merge-unparseable-subject-receipt-gap-governance

- issue_id: `I-20260411-0217-A`
- title: `Protected-merge unparseable-subject receipt-gap governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `protected-merge-unparseable-subject-receipt-gap-governance`
- issue-name: `protected-merge-unparseable-subject-receipt-gap-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260411T141600Z/candidates.md#c-20260411-0217-a`
- source_brainstorm: `docs/B1-docs/raw-20260411T141600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
  - `docs/system/workspace/scripts/quality/governance-check`
  - `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- created_at: `2026-04-11`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` is red on a real protected-ancestry receipt-gap class that the existing owner intentionally left out of scope: six trailerless ancestry merges under `test-pre-merge-20260410-preferred-auth-fix` have generic subjects (`Merge`, `Merge fix`, `Merge updates`, `Merge complete pre-brainstorm`) and therefore cannot be validated by the current subject-matched backfill contract.

The current fail-closed behavior is correct, but Freely now needs a narrower follow-on owner so this history class can be audited without degrading protected-merge semantics into a hash-only exception list.

## Scope

1. Freeze a stronger explicit evidence schema for trailerless protected-ancestry merges whose subject is not parseable into source/target truth.
2. Extend `governance-check` to validate that new schema while preserving the existing parseable-subject receipt-gap path unchanged.
3. Keep the new path narrow to ancestry merges later absorbed by a trailer-bearing protected batch merge.
4. Add focused regressions for the new passing case and multiple malformed or underspecified rejection cases.
5. Record the April 10 preferred-auth ancestry chain using the new contract only after parser and tests are in place.

## Non-Goals

1. Do not weaken canonical trailer requirements for future protected merges.
2. Do not accept raw hash-only ledger entries.
3. Do not reopen the entire ordinary protected-merge receipt-gap policy.
4. Do not mix this lane with preferred-auth implementation work or unrelated runtime governance.
5. Do not infer canonical source/target truth from unstable topology alone.

## Acceptance

1. Freely defines a distinct validation path for unparseable-subject ancestry gaps that requires stronger evidence than commit hash plus free-text refs.
2. Existing parseable-subject receipt-gap behavior remains intact, including trailer-bearing merge rejection and source-branch policy checks.
3. `governance-check` still fails closed when the new entry shape is malformed, under-evidenced, or points at the wrong absorbing protected merge.
4. The April 10 preferred-auth ancestry chain can be represented canonically only through the new stronger-evidence path.
5. Focused regressions cover at least one valid generic-subject passing case and at least three rejection cases that would otherwise create audit bypass risk.

## IBM Handoff

- implementation_scope_summary:
  - `I-20260411-0217-A` owns only the new unparseable-subject ancestry-gap contract.
  - Prefer an explicit `validation_mode` in the existing ledger unless implementation evidence proves a separate ledger is materially safer.
  - Do not touch canonical ledger entries for the April 10 preferred-auth batch until tests and parser changes are both green.
- required_doc_refs:
  - `docs/B1-docs/raw-20260411T141600Z/brainstorms.md`
  - `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/brainstorms/b-protected-merge-unparseable-subject-receipt-gap-governance.md`
  - `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/prd.md`
  - `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/pre-tests.md`
  - `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/tasks.md`
  - `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
  - `docs/system/workspace/scripts/quality/governance-check`
  - `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

## Next

1. next_action: `completed`
2. revisit_trigger: Reopen only if canonical `develop` later loses the explicit stronger-evidence path for generic-subject ancestry gaps, or if new history classes prove this owner boundary is still too broad.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260411T141600Z/brainstorms.md`
- `docs/B1-docs/raw-20260411T141600Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/prd.md`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/pre-tests.md`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-protected-merge-unparseable-subject-receipt-gap-governance.md`
- `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/code-reviews/20260411-protected-merge-unparseable-subject-receipt-gap-verification.md`
- `docs/B2-docs/ibm/protected-merge-unparseable-subject-receipt-gap-governance/code-reviews/20260411-protected-merge-unparseable-subject-receipt-gap-canonical-closeout-verification.md`
