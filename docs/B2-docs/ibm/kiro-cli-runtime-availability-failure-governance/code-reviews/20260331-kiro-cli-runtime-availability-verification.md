# Verification: kiro-cli-runtime-availability-failure-governance

- issue_id: `I-20260331-1830-A`
- reviewer: `codex`
- verdict: `pass_for_closeout`

## Commands

- `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `./bin/governance-check`

## Results

1. `Monthly request limit reached` is now written as `kiro_monthly_request_limit` instead of falling through to `ai_exit_rc_0`.
2. `Unable to verify subscription status: service error` alone is still treated as a canonical Kiro availability failure via `kiro_subscription_status_service_error`.
3. After either reason is detected, the local supervisor stops and defers availability recovery to the watchdog / manager control plane rather than relaunching immediately.
4. The focused regression proves the contract on a minimal fixture path and fails if the event log records a healthy `ai_exit_rc_0`.
5. `docs/system/workspace/tools.md` and `docs/system/workspace/skills/ai-cli-availability-manager/references/limit-patterns.md` now document the same Kiro failure family, so the behavior is no longer trapped only in runtime code.
6. The implementation itself was already absorbed by `develop` commit `3a6b0e0`; this artifact closes the canonical owner lifecycle around that landed fix.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
