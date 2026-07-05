# Issue: cli-help-and-dry-run-contract-followthrough-governance

- issue_id: `I-20260405-2358-D`
- title: CLI help and dry-run contract followthrough governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `cli-help-and-dry-run-contract-followthrough-governance`
- issue-name: `cli-help-and-dry-run-contract-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-2358-d`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-cli-help-and-dry-run-contract-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/issues/worktree-helper-shell-source-compatibility-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

canonical CLI replay still exposes a narrow but important contract gap:

1. `wt-create --help` currently enters the creation path and can reach Git side effects before failing.
2. `wt-enter --help` and `wt-add --help` do not expose an explicit sourced-help success path.
3. `pr-merge-guarded --help` and top-level `freely --help` print usage but still signal error.
4. `ai switch codex --dry-run --format json` still runs the heavy auto-probe flow, so the output is not a bounded dry-run contract.

These are CLI-first product behaviors, not operator trivia. If the first-hop command contracts stay ambiguous, later end-to-end validation keeps mixing genuine product failures with avoidable surface noise.

## Scope

1. Make the audited help paths explicit, side-effect free, and success-returning when the operator is only asking for usage.
2. Freeze a deliberate top-level `freely --help` contract instead of relying on unknown-command fallback.
3. Make `ai switch codex --dry-run --format json` emit one stable machine-consumable result without triggering the full switch/probe side effects.
4. Add focused regression coverage for the repaired help and dry-run contracts.

## Non-Goals

1. Do not reopen fresh-project bootstrap, `.githooks`, or `baseline-status`/`status --project` scoping work.
2. Do not absorb runtime supervision, stale-pid repair, `restart`, `chat`, or `restore-work` behavior.
3. Do not widen into generic wrapper executable-bit packaging; that is already owned by the completed packaging lane.
4. Do not redesign the entire ai slot-selection policy; only bound the dry-run reporting path.

## Acceptance

1. `freely wt-create --help` exits `0`, prints usage, and does not attempt branch/worktree creation.
2. `source ./bin/wt-enter --help` and `source ./bin/wt-add --help` exit `0` with explicit usage text, while direct execution still rejects them.
3. `freely pr-merge-guarded --help` and `./bin/freely --help` exit `0` with deliberate usage output.
4. `./bin/ai --quiet --format json --dry-run switch codex` returns one stable JSON object that reflects saved-slot inventory and does not require long-running probe completion.
5. Focused regressions and governance checks pass in the dedicated feature worktree.

## Verification

- `freely wt-create --help`
- `bash -lc 'source ./bin/wt-enter --help'`
- `bash -lc 'source ./bin/wt-add --help'`
- `freely pr-merge-guarded --help`
- `./bin/freely --help`
- `./bin/ai --quiet --format json --dry-run switch codex`
- `./bin/governance-check`

## Closeout

- Canonical `develop` absorbed this owner through `test-pre-merge-20260406-0408-cli-help-dry-run-contract-followthrough` and guarded merge `cb46eabf`.
- Post-merge closeout verification on `develop` reconfirmed the repaired help surfaces and bounded dry-run JSON contract on `2026-04-09`.
- Future work should open a new owner if another first-hop command contract regresses; do not reopen this bounded lane for unrelated runtime or bootstrap drift.
