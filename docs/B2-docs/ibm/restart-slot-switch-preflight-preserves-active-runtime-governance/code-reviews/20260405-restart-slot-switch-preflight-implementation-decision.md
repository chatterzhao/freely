# Implementation Decision: restart-slot-switch-preflight-preserves-active-runtime-governance

- issue_id: `I-20260405-2055-A`
- issue_path: `docs/B2-docs/ibm/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- decision_date: `2026-04-05`
- decision_owner: `codex`

## Decision

Treat restart-time slot-switch preflight as a new follow-on owner instead of reopening either completed parent owner.

## Why

- `I-20260404-2148-A` completed a deliberately narrow contract for `freely start` plus status/doctor lock observability.
- `I-20260327-2006-A` completed the parent project-command taxonomy and explicitly requires future command-semantics changes to open a new lifecycle.
- The current change adds a new contract: when restart is blocked by an active shared lock, the currently healthy project runtime must be preserved.

## Consequences

1. `cmd_restart` now runs restart preflight before any project-local stop.
2. The owner may absorb bounded helper hardenings needed to keep that preserved-runtime contract truthful under supervision churn.
3. Verification must prove both command ordering and live-runtime preservation, not just shared helper unit behavior.
