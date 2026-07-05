# Pre-Tests: live-status-scan-summary-and-prompt-anchor-governance

## Unit
- acceptance target: `Do not invent a fake lower-level seam; the truthful behavior change only appears once prompt-anchor lookup and advisory scan-summary readback are exercised through the runtime script surfaces together.`
- testing layer: `unit`
- target environment: `feature/runtime-status-fast-latest-artifact-lookup-20260421`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes runtime-shell orchestration for prompt selection and live-status output together. A narrower fake unit seam would miss the actual contract that prompt anchors remain authoritative while scan summary stays advisory.`
- replacement_evidence: `Focused runtime regressions plus the owner verification artifact are the smallest truthful executable boundary for this owner.`

## Integration
- acceptance target: `Live-status keeps prompt-anchor current-state truth authoritative while exposing advisory scan summary from bounded patrol inventory without regressing daemon, patrol, or worker-launch behavior.`
- testing layer: `integration`
- target environment: `feature/runtime-status-fast-latest-artifact-lookup-20260421`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`.
8. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`.
9. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`.
10. Run `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`.
11. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
12. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `The authoritative guarded merge batch carries this owner through feature -> test-pre-merge -> develop without losing prompt-anchor truth or scan-summary observability.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260421-live-status-scan-summary`
- required evidence: `guarded premerge replay plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Use `test-pre-merge-20260421-live-status-scan-summary` as the authoritative guarded batch for this owner.
2. Replay the focused live-status, daemon, patrol, worker-launch, and governance regressions there.
3. Stage the owner verification artifact in the same guarded develop-bound merge.

## Real-Environment
- acceptance target: `Canonical develop replay proves daemon start still selects work and reaches standards-compliant Freely behavior while live-status surfaces prompt-anchor truth plus advisory scan summary.`
- testing layer: `real_environment`
- target environment: `canonical develop runtime plus recorded live replay`
- required evidence: `develop-side daemon replay, live-status output, and owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `Canonical develop replay no longer dies before prompt build: daemon start returned running status, generated a fresh startup prompt at .freely/run/prompt-20260421-020221.txt, and preserved the anchor-first / scan-summary contract on the same merged runtime path. Residual tool-runtime restart-storm evidence remains a separate runtime-ops risk, not a regression introduced by this owner.`

## Acceptance Items

### Prompt anchor remains authoritative on current-state status surfaces
- id: `prompt-anchor-authoritative-live-status`
- requirement: `When an explicit session prompt anchor exists, live-status and adjacent prompt-reference surfaces prefer that anchor over prompt-history guessing.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-3`
- case_design: `Create a session state with an explicit prompt anchor and a lexically later stale prompt file, then verify the runtime read paths keep the anchored prompt authoritative.`
- testcase_derivation: `This owner exists to stop prompt-history guessing from stealing current-state truth, so the direct derivation is the prompt-anchor preference regression paired with the owner verification artifact.`

### Live-status exposes advisory scan summary without replacing current-state truth
- id: `live-status-advisory-scan-summary`
- requirement: `Live-status exposes advisory scan-summary fields sourced from manager-task-source-scan-latest.json while preserving existing current-state and deep-ref surfaces.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Populate the bounded patrol inventory JSON and verify live-status emits advisory summary fields without dropping existing prompt or runtime state fields.`
- testcase_derivation: `The new behavior is intentionally narrow: read the existing scan JSON into advisory status output. The scan-summary regression is the smallest truthful executable derivation.`

### Existing daemon, patrol, worker-launch, and verification contracts remain intact
- id: `bounded-status-change-no-capability-regression`
- requirement: `The owner does not regress daemon runtime detach/shared status, bounded patrol triggers, worker launch linkage, or verification metadata contracts.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3,tasks.md#task-4`
- case_design: `Replay the focused daemon, patrol, worker-launch, and verification regressions after the status changes and confirm every adjacent contract still holds.`
- testcase_derivation: `The user explicitly required no Freely capability drop, so this owner needs an explicit non-regression acceptance item tied to the adjacent contract regressions it could have disturbed.`

### Guarded premerge replay proves develop merge adequacy
- id: `live-status-scan-summary-guarded-promote-adequacy`
- requirement: `The authoritative test-pre-merge batch carries a staged pass owner review artifact proving prompt-anchor truth and advisory scan-summary output survive the guarded path into develop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-4,tasks.md#task-5`
- case_design: `Merge the feature lane into test-pre-merge-20260421-live-status-scan-summary, rerun the focused regressions there, and stage this owner review artifact with the guarded develop-bound promote.`
- testcase_derivation: `The develop gate exposed the missing premerge adequacy seam directly, so this owner needs an explicit premerge-integration/develop-merge acceptance item backed by the staged verification artifact.`

### Develop-side replay proves daemon start still selects work and preserves freely behavior
- id: `develop-daemon-start-freely-behavior-preserved`
- requirement: `After merge into develop, daemon start still selects work, preserves standards-compliant Freely flow, and live-status surfaces prompt-anchor truth plus advisory scan summary on the canonical runtime path.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- surface_kind: `real_environment`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-5`
- case_design: `Run canonical develop daemon start and startup-state inspection on the merged runtime path, verify a fresh prompt is materialized, and confirm the same owner contract still governs anchor-first status and advisory scan-summary behavior.`
- testcase_derivation: `The user tightened success criteria to require develop-side daemon-start validation, so this item derives from the smallest truthful live replay: canonical develop daemon start plus startup artifact inspection on the guarded merged tree.`
