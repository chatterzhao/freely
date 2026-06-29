# Pre-Tests: cli-help-and-dry-run-contract-followthrough-governance

## Unit
- acceptance target: `Do not invent a fake unit boundary for a CLI contract followthrough whose smallest executable surfaces are already the audited command regressions.`
- testing layer: `unit`
- target environment: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner tightens command-surface behavior and lifecycle writeback, but it does not add a separately callable unit beyond the focused CLI regressions already asserted below.`
- replacement_evidence: `The smallest executable boundaries are the audited help-contract and dry-run regressions, which are captured at integration level.`

## Integration
- acceptance target: `Prove audited help invocations and bounded dry-run output remain stable on the owner lane before guarded completion judgment.`
- testing layer: `integration`
- target environment: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- required evidence: `command output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`.
2. Run `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`.
3. Run `./bin/ai --quiet --format json --dry-run switch codex`.
4. Run `./bin/governance-check`.
5. Run `git diff --check`.

## End-to-End
- acceptance target: `Preserve the lawful feature -> test-pre-merge -> develop chain for this bounded CLI contract owner rather than treating focused verification as implicit merge proof.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifacts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/cli-help-dry-run-contract-followthrough-20260406-0408` into `test-pre-merge-20260406-0408-cli-help-dry-run-contract-followthrough` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-20260406-0408-cli-help-dry-run-contract-followthrough` into `develop` via `freely pr-merge-guarded`.
3. Confirm canonical `develop` still carries the same help-contract and bounded dry-run semantics instead of reopening runtime or bootstrap owners.

## Real-Environment
- acceptance target: `Reserve post-merge tracked-root replay as a distinct surface instead of pretending feature-lane verification alone proves canonical closeout.`
- testing layer: `real_environment`
- target environment: `canonical develop in the tracked root`
- required evidence: `tracked-root replay plus canonical closeout verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `Protected publication and any later origin/develop followthrough happen after canonical develop absorbs the owner; this pre-tests file records the boundary rather than faking remote publication locally.`
- replacement_evidence: `Tracked-root replay on local canonical develop, plus governance-check and the canonical closeout verification artifact, prove the bounded owner remains absorbed without reopening implementation.`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Audited help invocations are explicit, side-effect free, and success-returning for usage-only paths.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`

### AT-002
- id: `AT-002`
- requirement: `ai switch codex dry-run output is stable and machine-consumable.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`

### AT-003
- id: `AT-003`
- requirement: `Governance gates remain green for the bounded owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`
