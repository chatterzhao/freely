# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

- date: 2026-03-26
- reviewer: Codex
- scope: detached control-plane survival after manager `auth_failure`
- verdict: pass

## What changed

1. `runtime/freely` now launches manager supervisor, interruption dispatcher, and manager watchdog with detached `nohup` semantics instead of fragile background/disown semantics.
2. Added a focused regression that proves manager `auth_failure` does not collapse the watchdog control-plane.

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-watchdog-live-during-active-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `./bin/governance-check`

## Findings

1. Current patch closes a real same-family acceptance gap: canonical `develop` had delegated intake piling up after manager `auth_failure` because no detached control-plane process remained alive to continue script-owned recovery.
2. Detached launch does not regress the existing watchdog lifecycle coverage; both the active-AI watchdog test and the rate-limit delegation test still pass.
3. This batch remains `in_verification` until `develop` replay confirms canonical runtime no longer drops to `stalled_without_runtime` after `auth_failure`.
