# Pre-Tests: verification-contract-and-premerge-adequacy-governance

## Unit
- acceptance target: `Keep the verification contract parser and state projection helpers narrow enough that missing metadata is surfaced as data rather than hidden in prompt prose.`
- testing layer: `unit`
- target environment: `feature/verification-contract-adequacy-governance-followthrough`
- required evidence: `focused parser/state projection regression or explicit lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes shell-runtime flow and governance docs, but does not introduce a separately callable unit boundary beyond the focused script regressions already asserted at higher layers.`
- replacement_evidence: `Focused runtime regressions in test-freely-worker-prompt-verification-metadata and test-freely-manager-worker-launch-linkage cover the smallest executable boundary that exists in this package.`

## Integration
- acceptance target: `Prove manager handoff, delegated intake, worker runtime state, and pretests gate all consume one shared verification contract during guarded promotion flow.`
- testing layer: `integration`
- target environment: `test-pre-merge-verification-contract-adequacy-gate-r2-20260409`
- required evidence: `command output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`.
4. Run `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`.
5. Run `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`.
6. Run `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`.
7. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Keep the protected merge path and same-line lifecycle evidence visible end to end without pretending this owner also covers post-merge human dogfood.`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded feature -> test-pre-merge -> develop merge receipts plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/verification-contract-adequacy-gate-materialization-20260409` into `test-pre-merge-verification-contract-adequacy-gate-r2-20260409` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-verification-contract-adequacy-gate-r2-20260409` into `develop` via `freely pr-merge-guarded`.
3. Materialize same-line owner evidence before `develop` push so the guarded push path cannot treat the implementation as a bare code change.

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `This owner does not require an additional dedicated real-environment test beyond the guarded develop-bound verification path. The protected push and later dogfood observation remain separate post-merge acceptance surfaces.`

## Acceptance Items

### Runtime verification metadata is parsed
- id: `runtime-verification-metadata-parser`
- requirement: `Worker prompt parsing returns owner issue, pre-tests path, required lanes, acceptance item ids, evidence level, target environment, and closeout gate as machine-readable fields.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`

### Worker launch writes verification contract state
- id: `worker-launch-verification-contract-state`
- requirement: `Manager delegated launch writes the verification contract into delegated intake and worker runtime state so recovery can continue from structured truth.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`

### Pretests gate enforces section schema
- id: `pretests-gate-four-section-schema`
- requirement: `pretests-gate rejects owner pre-tests files that omit required sections, required section scalars, or replacement evidence for not-applicable sections.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`

### Guarded premerge path survives adequacy contract
- id: `guarded-premerge-verification-contract`
- requirement: `The guarded feature -> test-pre-merge -> develop path preserves verification contract metadata and owner lifecycle evidence without bypassing protected-branch receipts.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the guarded feature -> test-pre-merge -> develop chain while keeping the canonical owner issue, progress, and review evidence in the same develop-bound diff.`
- case_design: `Use the guarded merge fixtures plus the owner-bound review artifact to prove develop promotion consumes explicit verification-contract adequacy truth rather than a bare implementation diff.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/code-reviews/20260412-real-environment-verdict-followthrough.md`
