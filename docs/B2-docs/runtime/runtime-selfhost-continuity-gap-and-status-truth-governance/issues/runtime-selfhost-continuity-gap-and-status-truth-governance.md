# Issue: runtime-selfhost-continuity-gap-and-status-truth-governance

- issue_id: `I-20260407-0215-A`
- title: Runtime self-host continuity gap and status truth governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-selfhost-continuity-gap-and-status-truth-governance`
- issue-name: `runtime-selfhost-continuity-gap-and-status-truth-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260407T103600Z/candidates.md#c-20260407-0215-a`
- source_brainstorm: `docs/B1-docs/raw-20260407T103600Z/brainstorms.md`
- execution_base: `feature/runtime-live-status-and-manager-continuity-followthrough-20260407`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- verification_artifact_dir: `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/runtime/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
  - `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
  - `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

This owner was opened because canonical root `develop` showed a narrow but reusable self-host supervision gap:

1. the latest manager prompt explicitly requires a new continuity file
2. the latest generated continuity is still older than that prompt
3. delegated continuation evidence remains pending
4. status previously could degrade all the way to blank output when PID hint validation failed under `set -e`

This is not a CLI-first owner and not a generic watchdog redesign. It is the next bounded runtime followthrough after blocked-supervision truth: Freely must at least survive degraded PID truth, avoid PATH-sensitive workspace lookup, and expose the missing prompt-required continuity as machine-readable runtime state.

## Scope

1. Keep `live-status` readable when PID hint validation fails and only unverified or no process evidence is available.
2. Remove the hard `rg` dependency from project workspace-root selection so status and prompt assembly can degrade cleanly on PATH-constrained launches.
3. Surface named `manager_continuity_gap_*` fields in `live-status`, plus a continuity-gap summary row in `fleet-status`, when the latest prompt requires a manager continuity path that has not been materialized.
4. Distinguish fresh startup gaps from sustained missing continuity by surfacing gap age and writer-process evidence in runtime status, while allowing `fleet-status` to keep a summarized writer view.
5. Keep manager prompt guardrails aligned with this bounded owner so same-lane handoff reads the active feature-worktree owner docs and avoids `zsh` `status` variable collisions.
6. Tighten blocked-supervision and delegated-continuation discovery to read interruption-resolution artifacts directly, so the bounded status surfaces stay truthful without rescanning the full intake pool on every replay.
7. Add focused regressions for the PID-hint degrade path, the `rg`-missing fallback, the continuity-gap status surface, and the manager prompt guardrails above.

## Non-Goals

1. Do not redesign generic runtime restart orchestration.
2. Do not widen into full automatic repair of every missing manager continuity path.
3. Do not absorb the missing-worktree governance drift from unrelated progress artifacts unless it directly blocks this owner's bounded verification.
4. Do not reopen CLI help/dry-run, broad network taxonomy, or worker-stall recovery owners.

## Acceptance

1. `live-status` no longer exits blank when pid-file hints fail authoritative project validation.
2. `workspace_root_for_project()` chooses the project workspace without requiring `rg` in PATH.
3. `live-status` exposes named `manager_continuity_gap_*` fields, and `fleet-status` exposes a continuity-gap summary row, when a prompt-required continuity file is missing.
4. The continuity-gap surface includes enough age/process detail to distinguish a fresh bootstrap gap from a sustained self-host stall, with `live-status` carrying the full machine-readable writer-state and `fleet-status` keeping the summarized fleet view.
5. Focused regressions prove the new degrade path and continuity-gap surface without regressing existing blocked-supervision or core live-status coverage.

## Completion

- `docs/B1-docs/raw-20260407T103600Z/brainstorms.md`
- `docs/B1-docs/raw-20260407T103600Z/candidates.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/brainstorms/b-runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/prd.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/pre-tests.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/tasks.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-implementation-decision.md`
- `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`
- `docs/progress/workspace-routing-foundation/p-runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`
- `docs/system/workspace/scripts/tests/test-freely-live-status-pid-hint-and-rg-degrade`

## IBM Handoff

- implementation_scope_summary:
  - `I-20260407-0215-A` owns the bounded self-host runtime followthrough where prompt-required continuity does not materialize and status must surface that gap clearly.
  - The current implementation slice is allowed to touch runtime status logic, workspace-root fallback logic, interruption-resolution-backed status discovery for blocked-supervision and delegated continuation, manager prompt guardrails needed to keep same-lane owner handoff truthful, and focused regressions only.
  - Broad automatic recovery of missing continuity paths remains a follow-on decision unless the bounded status slice proves insufficient.
- required_doc_refs:
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/brainstorms/b-runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/prd.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/pre-tests.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/tasks.md`
  - `docs/B2-docs/runtime/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-pid-hint-and-rg-degrade`
- `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-feature-owner-doc-anchor`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-zsh-status-guard`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-blocked-supervision-status-surface`
- `./bin/governance-check`
- `git diff --check`
- `/usr/bin/time -p freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `cd /Users/zhaoyu/Downloads/code/my-freely/freely && /usr/bin/time -p freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Next

## Closeout

- Canonical `develop` already carries the bounded runtime status-truth repair and the tracked-root replay recorded parity with the original feature entrypoint.
- `2026-04-09` closeout verification reconfirmed focused regressions, governance, and pre-tests gate pass in a dedicated closeout worktree without reopening implementation scope.
- Future work should open a new owner if canonical `develop` regresses the pid-hint degrade path, the `rg`-missing fallback, or the continuity-gap status surface; do not reopen this bounded owner for separate runtime evidence provenance research.
