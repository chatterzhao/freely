# Brainstorm: runtime-forensic-time-alignment-and-stall-recovery-observability-governance

## Framing

The original confusion in the 2026-04-12 manager-stall investigation came from mixing:

- UTC event timestamps from `runtime-events.log`
- host-local file mtimes from prompt / cycle log / jsonl
- hidden runtime recovery residue in `.freely/run/preemption-state.env`

That did not prove the display-time owner wrong. It proved the runtime observation contract still allowed a real recovery to be invisible in the canonical event plane.

## Decision

This should land as a new narrow owner, not a reopen of the display-time owner and not a reopen of the already completed generic observation contract.

Reason:

1. The fix is bounded and runtime-specific.
2. The user-facing display boundary is already frozen and still correct.
3. The immediate product risk is incident misdiagnosis, not wrong timestamp rendering.

## Owner Boundary

### In scope

- explicit runtime event emission for stall recovery
- issue-bound writeback for the current continuity fallback repair
- freezing the governance distinction between display-time policy and forensic alignment policy

### Out of scope

- broad run-id redesign across every artifact
- turning every artifact into dual local/UTC output
- generic restart policy redesign

## Verification Shape

The smallest convincing evidence set is:

1. a focused shell regression that forces stalled-manager recovery and now observes the runtime event ledger
2. a focused shell regression that proves `freely stop` materializes the missing manager continuity required by the latest prompt
3. one issue-bound implementation decision note explaining why this is observation scope, not display scope
