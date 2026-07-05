# Pre-Tests: runtime-network-failure-taxonomy-and-bounded-recovery-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `runtime network failure taxonomy and bounded recovery`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: runtime classification plus bounded retry/cooldown coverage without fallback regression
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Runtime distinguishes `oauth_unreachable` from execution-time network failures.
2. Execution-time network failures are classified as `execution_network_transient`, `execution_network_persistent`, or `proxy_config_invalid`.
3. Network-local execution failures do not trigger slot rotation or cross-tool fallback by default.
4. During an active retry/cooldown window, manager recovery stays blocked on the current `tool + slot`.
5. After the retry window expires, manager recovery relaunches the same current `tool + slot`.
6. Existing slot-first and cross-tool fallback regressions remain green, proving this slice does not regress slot/tool availability behavior.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries bounded in-place network recovery truth`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner must close once develop carries the bounded retry/cooldown network taxonomy.
2. Canonical truth must continue to state that network-local failures do not rotate slot or tool by default.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `runtime classifies execution-time network failures into canonical bounded-recovery reasons`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`

### PT-2
- id: `PT-2`
- requirement: `network-local failures block slot and cross-tool fallback during retry window`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-blocks-fallback`

### PT-3
- id: `PT-3`
- requirement: `retry window expiry relaunches the same current tool plus slot`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-relaunches-current-slot`

### PT-4
- id: `PT-4`
- requirement: `slot-first and cross-tool fallback regressions remain green after network taxonomy changes`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-network-failure-taxonomy-and-bounded-recovery-governance/code-reviews/20260401-runtime-network-failure-taxonomy-and-bounded-recovery-verification.md`
