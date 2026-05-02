# Issue: manager-startup-continuity-materialization-governance

- issue_id: `I-20260413-0420-D`
- title: `Manager startup continuity materialization governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-startup-continuity-materialization-governance`
- issue-name: `manager-startup-continuity-materialization-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/candidates.md#c-20260413-0420-d`
- source_brainstorm: `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-startup-continuity-materialization-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews`
- follow_on_to: `I-20260413-0420-B`
- created_at: `2026-04-13`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` now has the two prerequisite truths for this lane:

1. startup authority/readiness is already authoritative, so launch truth no longer depends on PID or argv resemblance
2. the manager startup contract already froze `launch_bootstrapped` versus `manager_handoff_materialized`
3. the runtime already knows the prompt-required continuity path before AI launch
4. stop fallback already knows how to write a repair continuity file, but normal startup still does not write a first handoff artifact on success

That leaves Freely with a narrow but real product defect: the outer loop can be bootstrapped without a launch-bound first continuity artifact, so normal startup still relies on later manager behavior or stop repair to materialize the handoff chain.

## Scope

1. Seed a launch-bound manager continuity stub at the prompt-required path on the normal startup path.
2. Make the runtime-written startup stub distinguishable from stop-time repair fallback and from manager-materialized continuity.
3. Surface machine-readable manager handoff state in `live-status`.
4. Surface the same bounded handoff state in `fleet-status` when the current state is not yet `materialized`.
5. Add focused regressions for startup stub materialization and handoff-state surfacing.

## Non-Goals

1. Do not redefine `daemon start` readiness around manager continuity in this owner.
2. Do not widen into generic watchdog, restart, or worker handoff redesign.
3. Do not invent a new artifact family when the expected continuity path seam already exists.
4. Do not treat stop fallback as normal startup evidence.

## Acceptance

1. After prompt assembly and before AI launch, runtime materializes the expected continuity path with a launch-bound startup stub when the file is still absent.
2. The startup stub is labeled so status can classify it separately from `freely-runtime-fallback` repair artifacts and from manager-written continuity.
3. `live-status` exposes `manager_handoff_state`, `manager_handoff_reason`, `manager_handoff_expected_path`, `manager_handoff_latest_generated`, `manager_handoff_prompt_file`, `manager_handoff_writer`, and `manager_handoff_summary`.
4. `fleet-status` exposes a bounded manager handoff summary row whenever the state is not `none` and not yet `materialized`.
5. Focused regressions prove normal-path stub materialization and handoff-state surfacing, while the existing stop fallback regression still proves repair-only behavior.

## IBM Handoff

- implementation_scope_summary:
  - This owner materializes the first normal-path startup continuity artifact using the existing expected continuity seam in `runtime/freely`.
  - The implementation remains bounded: write a startup stub if the prompt-required file is absent, classify the observed handoff artifact by writer/source, and surface that classification in status.
  - Startup authority/readiness remains owned by `I-20260413-0420-A`; manager continuity contract shape remains owned by `I-20260413-0420-B`.
- required_doc_refs:
  - `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/brainstorms.md`
  - `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/candidates.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/issues/manager-startup-continuity-contract-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/brainstorms/b-manager-startup-continuity-materialization-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/tasks.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`
  - `docs/system/workspace/scripts/tests/test-freely-live-status-manager-handoff-state-surface`
  - `docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`
  - `docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`

## Verification

- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-closeout-verification.md`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-handoff-state-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`
- `./bin/governance-check`
- `git diff --check`

## Completion

- `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/candidates.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/brainstorms/b-manager-startup-continuity-materialization-governance.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/prd.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-closeout-verification.md`
- `docs/progress/workspace-routing-foundation/p-manager-startup-continuity-materialization-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`
- `docs/system/workspace/scripts/tests/test-freely-live-status-manager-handoff-state-surface`

## Next

- This owner should remain closed once canonical `develop` carries the startup stub materialization, handoff-state surface, and closeout verification artifact.
- Reopen only if canonical runtime later regresses back to prompt-only startup continuity or stop-fallback-as-normal-path behavior.
