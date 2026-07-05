# Issue: governance-merge-gate-review-aware-regression-alignment-governance

- issue_id: `I-20260404-0232-A`
- title: Governance merge gate review-aware regression alignment governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `governance-merge-gate-review-aware-regression-alignment-governance`
- issue-name: `governance-merge-gate-review-aware-regression-alignment-governance`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/candidates.md#c-20260404-0232-a`
- source_brainstorm: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- reopen_reason: `post-merge acceptance proved the mixed unresolved-candidate implementation regression still uses a fixture from before staged review artifacts became mandatory`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-merge-gate-review-aware-regression-alignment-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
  - `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`test-governance-merge-gate` still carries a mixed unresolved-candidate implementation case from before staged owner review artifacts became mandatory. Once `I-20260401-2354-A` landed, that fixture started failing earlier on missing review evidence.

Reproducing the current path shows the canonical contract is different from the old expectation: unresolved `needs_research` candidate metadata repairs are allowed to travel inside the same governance owner line when the merge already carries same-line issue/progress/review evidence. The same inspection also exposed a real same-file bypass in `governance-merge-gate`: directly touched `promoted` / `absorbed` candidates could share a `candidates.md` file with the true owner candidate and incorrectly skip owner-binding validation.

Post-merge acceptance on canonical `develop` therefore needs a narrow realignment owner that does two things at once: refresh the allowed unresolved-candidate fixture and restore the documented borrowed-owner block for same-file `promoted` / `absorbed` regressions.

## Scope

1. Refresh the mixed unresolved-candidate implementation fixture in `test-governance-merge-gate` so it stages a complete owner review artifact before asserting pass.
2. Remove the file-scope borrowed-owner bypass so directly touched same-file `promoted` / `absorbed` candidates still require their own canonical owner evidence.
3. Keep the expected results on the current allowed unresolved-candidate path and the documented blocked borrowed-owner path.
4. Record the narrow reopen lifecycle required by this post-merge acceptance finding.

## Non-Goals

1. Do not redesign `governance-merge-gate` policy beyond restoring the documented borrowed-owner block and the current unresolved-candidate allowance.
2. Do not relax the staged review artifact or implementation decision note requirement.
3. Do not widen this owner into a full diagnostic wording or merge-gate policy sweep.

## Acceptance

1. The implementation-bearing mixed unresolved-candidate case stages a valid review artifact for the same-line owner and passes.
2. Same-file `promoted` / `absorbed` borrowed-owner regressions fail with the concrete owner diagnostic.
3. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` passes.
4. `./bin/governance-check` passes.

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `git diff --check`
- `./bin/governance-check`

## Next

- `2026-04-04` closeout: canonical `develop` already absorbed this narrow review-aware regression alignment through merge `0bb78ce`.
- Keep this owner closed as the bounded mixed-regression and borrowed-owner realignment record; future merge-gate residuals must reopen as new owners on current `develop`.
