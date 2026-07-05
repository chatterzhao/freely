# Brainstorm: runtime-human-readable-time-display-governance

## Problem

The repo already proved the right time boundary, but runtime/workspace surfaces still apply it inconsistently. Probe activity, `freely ai`, and watchdog cooldown text already format display time in the host timezone, while `freely live-status`, `baseline-status`, intake status, and `develop-push status` still expose raw ISO/UTC values directly to humans.

## Boundary

- Keep naming truth in UTC.
- Keep stored truth in epoch / RFC3339 / ISO.
- Format only human-readable status surfaces into host-local time with timezone label.

## Why A Dedicated Owner

- `frontend-probe-v0` should not absorb runtime/workspace status surfaces.
- The code already crossed multiple surfaces and now needs canonical lifecycle ownership.
- This slice is narrow enough to verify directly without reopening a larger timezone umbrella.

## Delivery Shape

1. Add a shared runtime helper for display formatting.
2. Route `freely live-status`, `baseline-status`, intake status, and `develop-push status` through it.
3. Keep `ai-cli` and watchdog as part of the same display contract.
4. Prove with fixed `TZ=America/Los_Angeles` fixtures that human output is local while stored truth remains ISO/UTC/epoch.
