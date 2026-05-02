# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

- date: 2026-03-26
- reviewer: Codex
- scope: interruption dispatcher ready gate and watchdog status surface
- verdict: pass

## What changed

1. `cmd_start()` now treats interruption dispatcher readiness as a hard bootstrap gate.
2. `live-status` now treats a live manager watchdog as active control-plane and surfaces it as `role=manager_watchdog`.
3. Added focused regressions for watchdog-only status surface and dispatcher-not-ready startup failure.

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`

## Findings

1. This batch closes a real same-family acceptance drift: canonical control-plane could be alive while `live-status` omitted watchdog and misled supervision.
2. Startup now refuses to continue with a partial control-plane if interruption dispatcher fails to become ready.
3. Completion remains pending develop replay and manager absorption; this batch is `in_verification`, not completed.
