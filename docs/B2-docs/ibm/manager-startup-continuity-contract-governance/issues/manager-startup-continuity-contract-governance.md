# Issue: manager-startup-continuity-contract-governance

- issue_id: `I-20260413-0420-B`
- title: `Manager startup continuity contract governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-startup-continuity-contract-governance`
- issue-name: `manager-startup-continuity-contract-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260413-0420/candidates.md#c-20260413-0420-b`
- source_brainstorm: `docs/B1-docs/raw-20260413-0420/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-startup-continuity-contract-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews`
- follow_on_to: `I-20260413-0420-A`
- created_at: `2026-04-13`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` now has authoritative startup identity and launch-bootstrapped truth, but manager startup still lacks a frozen contract for the first handoff artifact:

1. the prompt requires a new manager continuity path, yet runtime only observes that path after prompt publication
2. normal startup still treats `AI launched` as sufficient even when the expected continuity does not materialize until stop fallback
3. `live-status` exposes continuity-gap truth, but does not yet expose a canonical `bootstrapped` versus `manager_handoff` boundary
4. without a frozen contract, future fixes will keep mixing prompt wording, status surfaces, and stop repair instead of repairing one bounded seam

This owner is the contract-freezing follow-on to startup authority. It decides what must change next without pretending the runtime implementation is already landed.

## Scope

1. Freeze that manager startup has two distinct success layers: `launch_bootstrapped` and `manager_handoff_materialized`.
2. Freeze that the normal startup path must materialize a launch-bound first handoff artifact instead of relying on stop fallback.
3. Freeze that the preferred first implementation shape is a runtime-seeded continuity claim/stub at the expected manager continuity path, followed by manager enrichment.
4. Freeze that runtime status surfaces must expose machine-readable manager handoff state distinct from launch bootstrapping.
5. Keep stop-time continuity materialization explicitly repair-only.
6. Write canonical owner, milestone, and progress truth so future implementation can start from `develop` without reopening this root-cause analysis.

## Non-Goals

1. Do not implement the continuity stub writer, status fields, or daemon/readiness changes in this owner.
2. Do not widen startup authority/readiness to block `daemon start` on manager continuity in this first contract pass.
3. Do not treat prompt wording alone as the fix for first-handoff materialization.
4. Do not reopen worker continuity consumption, delegated continuation stall recovery, or generic watchdog redesign from this owner.

## Acceptance

1. Canonical docs distinguish `launch_bootstrapped` from `manager_handoff_materialized` as separate runtime truths.
2. Canonical docs freeze that the first manager handoff artifact must be created on the normal startup path and must not depend on stop fallback.
3. Canonical docs freeze that the preferred initial implementation shape is `runtime-seeded continuity claim/stub -> manager enrich`, not prompt-only best effort.
4. Canonical docs freeze that status must expose a machine-readable handoff state without immediately redefining `daemon start` readiness.
5. The bounded owner lands on `develop` as issue/progress/review/pre-tests truth without editing runtime capability files.

## IBM Handoff

- implementation_scope_summary:
  - This owner freezes the manager startup handoff contract and the first implementation seam, but intentionally stops before runtime code changes.
  - The follow-on implementation owner should start from the frozen contract here: runtime seeds the expected continuity artifact on the normal path, manager enriches it, status exposes handoff state, and stop fallback remains repair-only.
- required_doc_refs:
  - `docs/B1-docs/raw-20260413-0420/brainstorms.md`
  - `docs/B1-docs/raw-20260413-0420/candidates.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/brainstorms/b-manager-startup-continuity-contract-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/tasks.md`
  - `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-decision.md`

## Verification

- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-decision.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-verification.md`
- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`
- `git diff --check`

## Completion

- `docs/B1-docs/raw-20260413-0420/candidates.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/issues/manager-startup-continuity-contract-governance.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/brainstorms/b-manager-startup-continuity-contract-governance.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/prd.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-decision.md`
- `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-verification.md`
- `docs/progress/workspace-routing-foundation/p-manager-startup-continuity-contract-governance.md`
- `docs/milestones.md`

## Next

- This owner should remain closed once canonical `develop` carries the frozen startup-handoff contract.
- Open a new implementation owner when runtime is ready to add the normal-path continuity stub and machine-readable handoff state surfaces.
