# Pre-tests - preferred-auth-method-account-switch-fix

## Unit

- `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
  - Verifies account switch sets `preferred_auth_method = "chatgpt"`
  - Verifies apikey switch sets `preferred_auth_method = "apikey"`

## Integration

- Cross-kind switch preserves config tables correctly

## End-to-End

- Existing `test-freely-ai-account-switch` covers full switch flow

## Real-Environment

- Dogfooding confirmed fix works

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `switching to account slot sets preferred_auth_method = "chatgpt"`
- evidence_level: `unit`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`

### PT-2
- id: `PT-2`
- requirement: `switching to apikey slot sets preferred_auth_method = "apikey"`
- evidence_level: `unit`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`