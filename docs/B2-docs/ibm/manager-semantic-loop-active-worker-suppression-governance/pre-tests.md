# Pre-Tests: manager-semantic-loop-active-worker-suppression-governance

## Acceptance Targets

### AT-001 active worker execution suppresses semantic-loop suspicion

- acceptance target: the semantic-loop regression still detects the zero-worker loop shape, but clears once worker supervisor and AI execution are already active
- testing layer: integration
- target environment: feature worktree runtime scripts plus focused regression
- required evidence: `semantic-loop regression replay`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 adjacent status surfaces stay stable

- acceptance target: `live-status` and `fleet-status` keep their current runtime/status surfaces healthy while the suppression fallback is active
- testing layer: integration
- target environment: feature worktree runtime scripts
- required evidence: `status regression replay`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 closeout stays bounded to semantic-loop suppression

- acceptance target: lifecycle truth records the new follow-on owner without reopening completed `I-20260322-0445` or widening into unrelated stall recovery
- testing layer: IBM review
- target environment: issue/progress/milestone artifacts
- required evidence: `issue + progress + milestone + implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Semantic-loop monitoring clears once active worker execution is already present while preserving the zero-worker signal path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Adjacent live-status and fleet-status regressions remain green after the suppression fallback lands.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The closeout lane materializes a new bounded owner instead of reopening completed I-20260322-0445.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-implementation-decision.md`
