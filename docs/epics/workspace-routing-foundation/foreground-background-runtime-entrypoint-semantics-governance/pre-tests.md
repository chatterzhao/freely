# Pre-Tests: foreground-background-runtime-entrypoint-semantics-governance

## Unit
- acceptance target: `Keep existing foreground command parsing and new daemon command routing deterministic and explicitly separated.`
- testing layer: `unit`
- target environment: `feature/runtime-daemon-semantics`
- required evidence: `focused runtime command semantics output`
- blocker taxonomy: `definition_missing`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`.
2. Add and run a focused daemon command parsing regression.

## Integration
- acceptance target: `Foreground and daemon runtime paths share one runtime truth while preserving their distinct ownership contracts.`
- testing layer: `integration`
- target environment: `feature/runtime-daemon-semantics`
- required evidence: `runtime command output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`.
3. Add and run daemon-focused regressions for start persistence, explicit stop, and shared status truth.
4. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A daemon-started runtime stays alive after the launching shell exits, while a foreground start still stops on explicit operator interruption.`
- testing layer: `end_to_end`
- target environment: `feature/runtime-daemon-semantics`
- required evidence: `manual or scripted detached-session replay captured in verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Capture one foreground `freely start` replay with expected operator stop semantics.
2. Capture one detached `freely daemon start` replay that survives parent shell exit and requires explicit daemon stop.

## Real-Environment
- acceptance target: `This owner does not need a separate hosted environment; the runtime/session boundary is fully exercised on the local machine.`
- testing layer: `real_environment`
- target environment: `local runtime boundary`
- required evidence: `local detached-session replay recorded in verification artifact`
- blocker taxonomy: `definition_missing`
- real_environment_status: `pass`
- real_environment_reason: `The bounded executable surface is the local runtime/session ownership boundary, and the detached daemon replay was exercised directly in the scripted feature-local and premerge-integration verification runs.`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The contract change is about local runtime/session ownership rather than an external hosted surface.`
- replacement_evidence: `Local detached-session runtime replay plus focused runtime regressions are sufficient for this bounded owner.`

## Acceptance Items

### Foreground contract remains stable
- id: `foreground-contract-stable`
- requirement: `Existing foreground start/restart/stop/status semantics remain intact after daemon support is introduced.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Preserve current foreground command semantics and keep the existing foreground regressions passing.`
- case_design: `Replay the existing command-semantics, event-log, and stop-all-supervisors tests without converting them into daemon tests.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`

### Daemon survives parent shell exit
- id: `daemon-parent-session-detach`
- requirement: `A daemon-started runtime keeps running after the launching shell or PTY exits and no longer records the stop as a foreground operator stop.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Add explicit daemon start behavior with detached-session ownership and prove it survives parent session teardown.`
- case_design: `Launch daemon mode from a short-lived shell, terminate the launcher, confirm the runtime still reports running, then stop it explicitly.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`

### Shared status truth remains singular
- id: `daemon-shared-status-truth`
- requirement: `Foreground and daemon entrypoints continue to report runtime state through the same underlying status and log truth surfaces.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Keep daemon status and logs wired to the existing runtime state files and status commands rather than adding a separate state family.`
- case_design: `Compare daemon status/log outputs with live-status or fleet-status for the same project runtime and confirm they agree on running/stopped state.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`

### Guarded develop promote proves daemon adequacy
- id: `develop-promote-daemon-entrypoint-proof`
- requirement: `A guarded test-pre-merge promote proves this owner carries explicit premerge-integration coverage for develop-bound merge rather than relying only on feature-local daemon completion evidence.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the daemon-focused verification batch on a disposable test-pre-merge branch created from develop, and use that replay to prove guarded promotion adequacy for the explicit daemon control plane.`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch through pr-merge-guarded, rerun the foreground and daemon regressions plus governance-check there, and use the resulting verification artifact to prove the develop-bound lane/gate pair is explicitly covered.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-closeout-verification.md`
