# Issue: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

- issue_id: `I-20260405-2358-A`
- title: Fresh-project bootstrap and baseline scoping followthrough governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `fresh-project-bootstrap-and-baseline-scoping-followthrough-governance`
- issue-name: `fresh-project-bootstrap-and-baseline-scoping-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-2358-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
  - `docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
  - `docs/system/workspace/scripts/runtime/freely`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical CLI replay on `develop` proved a narrow but blocking bootstrap defect remains after the earlier worktree/bootstrap owners closed:

1. `freely sync-tooling --source-project <repo> --project <fresh-git-project>` copies source-root config truth directly into the target project, so `PROJECT_ROOT`, `INTENT_FILE`, and `CONSTITUTION_FILE` can keep pointing at the source repo.
2. The same sync path does not rematerialize `.githooks`, so a later `freely init` on the fresh project still fails the hook gate unless the operator copies hooks by hand.
3. Because the target config is mis-scoped, `freely baseline-status --project <x>` and the baseline view of `freely status --project <x>` drift back to the source project instead of the requested target.

This is a first-hop CLI contract bug. If fresh-project bootstrap is wrong, every later project-targeted command replay becomes hard to trust.

## Scope

1. Repair `sync-tooling` so target-local config truth is rewritten to the target project instead of preserving source-root absolute paths.
2. Rematerialize `.githooks` into fresh git targets when the source project already owns the managed hook surface.
3. Add focused behavior coverage proving `baseline-status` and `status --view baseline` stay pinned to the target project after sync and after a follow-on `init`.
4. Keep `ensure-interruption-dispatch --project <x>` in scope only as a non-regression boundary for “semantic doc gate failure, not raw filesystem noise”.

## Non-Goals

1. Do not reopen runtime/control-plane churn from `start` / `restart` / `chat` / `restore-work`.
2. Do not widen into general help/dry-run CLI ergonomics or ai switch semantics.
3. Do not redesign activation-consent or per-tool authorization architecture; this owner only consumes those upper-bound truths.
4. Do not turn `sync-tooling` into a generic full-project clone mechanism beyond the managed bootstrap surfaces.

## Acceptance

1. `freely sync-tooling --source-project <repo> --project <fresh-git-project>` leaves target `.freely/config.env` pinned to `<fresh-git-project>`, not `<repo>`.
2. The same command materializes `.githooks` when the source project has them, so `freely init` can continue without manual hook copying.
3. `freely baseline-status --project <fresh-git-project>` reports `project`, `intent`, and `constitution` for the target project.
4. `freely status --project <fresh-git-project> --view baseline` reports the same target-local baseline truth.
5. Focused behavior tests and a real fresh-project CLI replay pass without reopening adjacent runtime owners.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-status-family`
- `./bin/governance-check`

## Completion

- `docs/B1-docs/raw-20260405/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- `docs/B2-docs/config/packaging/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`
- `docs/B2-docs/config/packaging/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-canonical-closeout-verification.md`
- `docs/progress/freely-product-architecture/p-fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`

## Next

- Completed on canonical `develop` after guarded promotion through `test-pre-merge-fresh-project-bootstrap-baseline-scoping-followthrough-20260406-1935` and closeout verification recorded in `docs/B2-docs/config/packaging/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-canonical-closeout-verification.md`.
- Reopen only if fresh-project sync stops retargeting baseline truth to the requested project, `.githooks` disappear again on sync/init replay, or baseline/status surfaces drift back to the source repo.
