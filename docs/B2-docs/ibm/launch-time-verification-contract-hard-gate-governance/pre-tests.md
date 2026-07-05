# Pre-Tests: launch-time-verification-contract-hard-gate-governance

## Unit
- acceptance target: `Keep verification metadata parsing and missing-field projection deterministic at the launch boundary.`
- testing layer: `unit`
- target environment: `feature/launch-time-verification-contract-hard-gate-20260411`
- required evidence: `focused parser/runtime regression output`
- blocker taxonomy: `definition_missing`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`.

## Integration
- acceptance target: `Manager dispatch refuses worker launch when required verification metadata is incomplete and preserves a machine-readable blocked diagnosis.`
- testing layer: `integration`
- target environment: `feature/launch-time-verification-contract-hard-gate-20260411`
- required evidence: `command output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`.
3. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A complete worker handoff still launches successfully after launch-time hard gate is enabled.`
- testing layer: `end_to_end`
- target environment: `feature/launch-time-verification-contract-hard-gate-20260411`
- required evidence: `successful complete-contract launch path plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Capture one complete-contract manager-to-worker launch in the verification artifact.

## Real-Environment
- acceptance target: `This owner does not require a separate real-environment run before implementation closeout; local runtime integration is the executable boundary.`
- testing layer: `real_environment`
- target environment: `local runtime boundary`
- required evidence: `lawful replacement evidence recorded in verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The launch hard gate is a runtime/governance boundary exercised by local integration tests; no additional hosted environment is introduced in this owner.`
- replacement_evidence: `Focused runtime regressions and one complete-contract launch capture are sufficient for this bounded owner.`

## Acceptance Items

### Missing metadata blocks launch
- id: `launch-missing-metadata-blocked`
- requirement: `Runtime refuses worker launch when any required verification metadata field is missing and records the missing-field list machine-readably.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Refuse manager-driven worker launch whenever the worker prompt omits required verification metadata and persist a machine-readable blocked state instead of silently starting the worker.`
- case_design: `Replay partial metadata and branch-only worker prompts, then confirm the worker contract file and workcell state retain the blocked reason plus missing-fields projection.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`

### Complete metadata still launches
- id: `launch-complete-metadata-pass`
- requirement: `A complete manager worker prompt still launches the target worker without regression.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Preserve the valid manager-to-worker handoff path while the launch boundary becomes fail-closed for incomplete verification contracts.`
- case_design: `Use a fully populated worker prompt to prove delegated intake materialization, runtime contract capture, and active-worker reentry still work after hard-gating is enabled.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`

### Branch-only fallback is explicitly resolved
- id: `branch-only-prompt-launch-policy`
- requirement: `Branch-only or natural-language prompts no longer silently bypass the verification contract; they are either rejected with guidance or upgraded through an explicit remediation path.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Block unresolved, branch-only, missing-prompt, and malformed recovery paths instead of reconstructing launch context from ambiguous discovery alone.`
- case_design: `Replay branch-only prompt, unresolved worktree, missing prompt, stale cache, and malformed recovery fixtures to prove the runtime now fails closed while preserving operator-facing diagnostics.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`

### Guarded develop promote proves launch-time adequacy
- id: `develop-promote-launch-gate-proof`
- requirement: `A guarded test-pre-merge promote proves this owner carries explicit premerge-integration coverage for develop-bound merge instead of relying only on feature-local completion evidence.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay guarded promotion on a disposable test-pre-merge batch and confirm the owner now carries a distinct develop-merge adequacy statement plus fresh staged review evidence for launch-time hard gating.`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch through pr-merge-guarded, rerun the launch-time regressions plus governance-check there, and use the resulting verification artifact to prove the develop-bound lane/gate pair is explicitly covered.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/code-reviews/20260411-launch-time-verification-contract-hard-gate-verification.md`
