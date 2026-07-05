# Pre-Tests: runtime-startup-self-healing-governance

## Unit
- acceptance target: `Do not invent a fake lower-level seam; the smallest executable boundaries here are focused runtime script regressions.`
- testing layer: `unit`
- target environment: `feature/live-status-hang-root-cause-20260422`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes runtime shell orchestration and status readback, so the lawful executable seams are the focused shell regressions and guarded replay below.`
- replacement_evidence: `Focused startup-self-heal and launch-state persistence regressions capture the smallest executable behavior changes.`

## Integration
- acceptance target: `Prove startup self-heal clears stale machine-owned truth without breaking adjacent status/continuity surfaces.`
- testing layer: `integration`
- target environment: `feature/runtime-startup-self-healing-followthrough-20260419`
- required evidence: `focused regression output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed`.
8. Run `bash docs/system/workspace/scripts/tests/test-freely-ai-pid-validation-supported-tools`.
9. Run `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal`.
10. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-active-manager-skips-fleet-refresh`.
11. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-uses-status-signals-when-manager-idle`.
12. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-count-fast-path`.
13. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
14. Run `bash docs/system/workspace/scripts/tests/test-freely-start-skips-preflight-slot-recovery-when-auto-switch-slot-disabled`.
15. Run `bash docs/system/workspace/scripts/tests/test-watchdog-manager-entry-skips-slot-selection-when-auto-switch-slot-disabled`.
16. Run `bash docs/system/workspace/scripts/tests/test-watchdog-probe-all-skips-sweep-when-auto-switch-slot-disabled`.
17. Run `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`.
18. Run `./bin/governance-check`.
19. Run `git diff --check`.

## End-to-End
- acceptance target: `Promote the bounded startup self-heal owner through canonical develop instead of treating feature-lane replay as final absorption.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifacts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/live-status-hang-root-cause-20260422` into canonical `develop` through a disposable `test-pre-merge-*` lane.
2. Push `develop` after final verification evidence is written back.
3. Delete the dedicated feature worktree and branch after develop carries the absorbed owner.

## Real-Environment
- acceptance target: `Use protected-root replay to prove stale startup truth self-heals under the real runtime entrypoint, not only in synthetic tests.`
- testing layer: `real_environment`
- target environment: `canonical protected root`
- required evidence: `protected-root live replay plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `Protected-root replay must confirm the post-L041 bootstrap grace repair lands on canonical develop so the manager lane no longer self-restarts immediately after ai_launch_observed.`
1. Inspect the protected root stale state before replay.
2. Run `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` and confirm startup self-heal canonicalizes stale machine state.
3. Run `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, wait through the startup grace window, and verify the runtime no longer remains in contradictory fake-up state.
4. Verify the detached supervisor survives after the non-interactive `daemon start` caller exits, instead of only staying alive while the caller shell/session remains open.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `startup status reads clear stale runtime pid files and downgrade stale startup truth when no authoritative runtime processes exist.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260419-runtime-startup-self-healing-verification.md`

### AT-002
- id: `AT-002`
- requirement: `launch-state continuity/prompt references are persisted after status refresh rewrites stale continuity anchors.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260419-runtime-startup-self-healing-verification.md`

### AT-003
- id: `AT-003`
- requirement: `protected-root replay proves the runtime no longer stays stuck in fake running/up startup truth after stale-machine-state cold start.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the followthrough fix through the guarded feature -> test-pre-merge -> develop lane and prove protected-root startup either self-heals stale state or remains in a live retryable supervisor state instead of collapsing to fake runtime absence.`
- case_design: `Merge the followthrough lane into a disposable test-pre-merge batch, rerun the focused startup-self-heal regressions there, explicitly verify AUTO_SWITCH_SLOT=false blocks startup/watchdog slot inventory and probing, then replay protected-root daemon start plus one-minute observation to confirm live-status and lifecycle evidence stay aligned for short-lived non-interactive CLI tools.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260423-runtime-startup-self-healing-disabled-slot-auto-switch-verification.md`
