# Pre-Tests: auth-switch-real-environment-and-e2e-adequacy-governance

## Unit
- acceptance target: `The auth/switch adequacy rule is represented in repo truth and can be evaluated by the gate without runtime path guessing`
- testing layer: `unit`
- target environment: `feature/auth-switch-pretests-governance-gap-analysis-20260410-171800`
- required evidence: `focused pretests-gate regression pass`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.

## Integration
- acceptance target: `IBM/checklist/gate truth all describe the same auth/switch dual-waive prohibition`
- testing layer: `integration`
- target environment: `feature/auth-switch-pretests-governance-gap-analysis-20260410-171800`
- required evidence: `aligned doc truth plus focused regression`
- blocker taxonomy: `execution_pending_or_failed`
1. Verify the updated IBM/checklist references and `pretests-gate` all carry the same auth/switch family rule.
2. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.

## End-to-End
- acceptance target: `A representative auth/switch follow-on owner that dual-waives End-to-End and Real-Environment without live evidence is rejected by the gate`
- testing layer: `end_to_end`
- target environment: `feature/auth-switch-pretests-governance-gap-analysis-20260410-171800`
- required evidence: `focused failing-then-passing gate replay in the regression suite`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
2. Confirm the regression covers the bad dual-waive pattern and the corrected pattern.

## Real-Environment
- acceptance target: `Auth-switch family owners are now required to preserve artifact-backed live executable evidence instead of legal dual-waivers`
- testing layer: `real_environment`
- target environment: `feature/auth-switch-pretests-governance-gap-analysis-20260410-171800`
- required evidence: `owner review cites real bin-ai, codex-exec, and freely-start evidence classes that the adequacy rule now protects`
- blocker taxonomy: `execution_pending_or_failed`
1. Audit the updated owner guidance and confirm it explicitly names real `bin/ai`, real `codex exec`, and real `freely start` as acceptable live evidence surfaces for this family.
2. Confirm the verification artifact explains why the earlier miss occurred and why those live surfaces now remain mandatory.

## Acceptance Items

### IBM truth forbids dual-waive without live evidence
- id: `AT-001`
- requirement: `Auth/switch/startup-recovery follow-on owners cannot dual-waive End-to-End and Real-Environment without artifact-backed live evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews/20260410-auth-switch-real-environment-and-e2e-adequacy-verification.md`

### pretests-gate blocks the bad pattern
- id: `AT-002`
- requirement: `pretests-gate rejects the auth-switch family when both sections are waived and no pass-level real_env or post_merge_dogfood acceptance item exists.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews/20260410-auth-switch-real-environment-and-e2e-adequacy-verification.md`

### Real executable evidence remains mandatory
- id: `AT-003`
- requirement: `The owner package records that real bin-ai, codex-exec, or freely-start evidence must remain on the acceptance surface for this family.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews/20260410-auth-switch-real-environment-and-e2e-adequacy-verification.md`
