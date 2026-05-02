# Pre-Tests: governance-check-protected-merge-history-source-policy-governance

## Acceptance Targets

### AT-001 develop audits only its canonical protected merge chain

- acceptance target: `governance-check` evaluates protected merge receipt source policy from first-parent branch history instead of all reachable merge ancestry
- testing layer: integration
- target environment: governance receipt audit
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `./bin/governance-check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Protected-branch source-policy auditing honors first-parent branch history.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-verification.md`
