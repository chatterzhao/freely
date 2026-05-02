# Pre-Tests: runtime-selfhost-continuity-gap-and-status-truth-governance

## Unit
- acceptance target: `Do not invent a fake unit boundary for a runtime status owner whose smallest executable seams are the focused status regressions and guarded shell parse replay.`
- testing layer: `unit`
- target environment: `feature/runtime-live-status-and-manager-continuity-followthrough-20260407`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner hardens runtime status surfaces and bounded prompt/continuity discovery, but it does not add a separately callable unit seam below the focused script regressions already tracked at integration level.`
- replacement_evidence: `The smallest executable boundaries are the audited live-status, continuity-gap, and prompt-guard regressions captured below.`

## Integration
- acceptance target: `Prove the bounded runtime status repair stays truthful under pid-hint degrade, rg-missing fallback, continuity-gap surfacing, and prompt guardrails before closeout.`
- testing layer: `integration`
- target environment: `feature/runtime-live-status-and-manager-continuity-followthrough-20260407`
- required evidence: `focused regression output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-pid-hint-and-rg-degrade`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`.
5. Run `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-feature-owner-doc-anchor`.
6. Run `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-zsh-status-guard`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
8. Run `bash docs/system/workspace/scripts/tests/test-freely-blocked-supervision-status-surface`.
9. Run `./bin/governance-check`.
10. Run `git diff --check`.

## End-to-End
- acceptance target: `Preserve the lawful feature -> test-pre-merge -> develop promote chain for this bounded runtime status owner instead of treating worker-lane replay as canonical absorption by itself.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifacts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-live-status-and-manager-continuity-followthrough-20260407` into its guarded `test-pre-merge-*` lane.
2. Merge that guarded batch into canonical `develop`.
3. Confirm tracked-root `develop` still carries the bounded status-truth surface instead of reopening worker implementation.

## Real-Environment
- acceptance target: `Reserve tracked-root entrypoint replay as a distinct canonical closeout check instead of pretending feature-lane status replay alone proves absorption.`
- testing layer: `real_environment`
- target environment: `canonical develop in the tracked root`
- required evidence: `tracked-root replay plus canonical closeout verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `Protected publication and any later origin/develop followthrough happen after canonical develop absorbs the owner; this pre-tests file records that boundary rather than faking remote publication locally.`
- replacement_evidence: `Tracked-root replay on local canonical develop, plus governance-check and the canonical closeout verification artifact, prove the bounded status-truth repair remains absorbed without reopening implementation.`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `live-status stays readable when pid-file hints fail authoritative validation.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`

### AT-002
- id: `AT-002`
- requirement: `workspace_root_for_project() no longer depends solely on rg being present in PATH.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`

### AT-003
- id: `AT-003`
- requirement: `live-status and fleet-status surface the bounded manager continuity gap truth with named machine-readable fields.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`

### AT-004
- id: `AT-004`
- requirement: `continuity-gap truth includes age and writer-state detail so startup grace is distinguishable from a sustained self-host stall.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`

### AT-005
- id: `AT-005`
- requirement: `manager prompt guardrails and blocked-supervision discovery remain green while this bounded status owner closes out.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`
