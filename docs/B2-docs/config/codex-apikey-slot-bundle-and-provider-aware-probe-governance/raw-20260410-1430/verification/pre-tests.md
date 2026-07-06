# Pre-Tests: preferred-auth-method-account-switch-fix

## Unit
- acceptance target: `Switching to account slot sets preferred_auth_method = "chatgpt"; switching to apikey slot sets preferred_auth_method = "apikey"`
- testing layer: `unit`
- target environment: `feature/preferred-auth-method-account-switch-fix-20260410-143000`
- required evidence: `test-ai-cli-codex-apikey-slot-bundle-switch pass`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`.

## Integration
- acceptance target: `Cross-kind account/apikey switch preserves preferred_auth_method correctly in live config`
- testing layer: `integration`
- target environment: `test-pre-merge-20260410-preferred-auth-fix`
- required evidence: `test pass plus config file verification`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`.

## End-to-End
- acceptance target: `Full switch flow from account to apikey and back preserves preferred_auth_method`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts plus test pass`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `The integration tests cover the full cross-kind switch flow; no separate end-to-end boundary exists for this narrow bug fix.`
- replacement_evidence: `test-ai-cli-codex-apikey-slot-bundle-switch and test-freely-ai-account-switch prove the switch flow works end to end.`

## Real-Environment
- acceptance target: `Dogfood confirms fix on local Freely runtime`
- testing layer: `real_environment`
- target environment: `origin/develop`
- required evidence: `protected branch push result`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `The canonical protected push happens only after develop carries both implementation and same-line owner evidence.`
- replacement_evidence: `Local guarded merge receipts plus governance-check prove readiness.`

## Acceptance Items

### Account switch sets preferred_auth_method to chatgpt
- id: `account-switch-preferred-auth-method`
- requirement: `Switching to account slot sets preferred_auth_method = "chatgpt" in live config`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`

### Apikey switch sets preferred_auth_method to apikey
- id: `apikey-switch-preferred-auth-method`
- requirement: `Switching to apikey slot sets preferred_auth_method = "apikey" in live config`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
