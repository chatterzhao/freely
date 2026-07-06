# Verification: preferred-auth-method-account-switch-fix

- issue_id: `I-20260410-1430-A`
- issue_path: `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/raw-20260410-1430issues/preferred-auth-method-account-switch-fix.md`
- verification_date: `2026-04-10`
- verifier: `codex`

## Scope Verdict

- `PASS`: switching to account slot now correctly sets `preferred_auth_method = "chatgpt"` in live config
- `PASS`: switching to apikey slot now correctly sets `preferred_auth_method = "apikey"` in live config
- `PASS`: existing cross-kind switch tests continue to pass
- `PASS`: new test assertion covers account switch behavior

## Commands

1. `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`

## Implementation Decision Note

- decision: `Add slot-kind-aware fallback in codex_apply_saved_slot_config_fragment to set preferred_auth_method when fragment doesn't provide it.`
- why_this: `The root cause was that account slots have empty config-auth.toml fragments, so preferred_auth_method was deleted but never restored during switch.`
- alternatives_considered: `Save preferred_auth_method in account slot fragments; modify save logic to always include preferred_auth_method; leave field unset and rely on Codex defaults.`
- boundary_non_goals: `No change to slot bundle architecture, no change to other tools, no reopening of I-20260405-0027-A scope.`
- residual_risk: `None. This is a narrow bug fix with no architectural implications.`