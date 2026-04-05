# Tasks: slot-switch-startup-preflight-and-lock-observability-governance

## Slice 1: Materialize the owner

- [x] Add the canonical issue for `I-20260404-2148-A`.
- [x] Add the matching progress artifact.
- [x] Add the issue-bound brainstorm, PRD, and pre-tests artifacts.

## Slice 2: Implement bounded startup preflight

- [x] Add shared lock snapshot helpers in `runtime/freely`.
- [x] Run startup preflight before supervisor bootstrap and clean only stale locks.
- [x] Fail or defer clearly when a live shared lock remains active.

## Slice 3: Expose lock truth

- [x] Surface current slot-switch lock truth in `doctor`.
- [x] Surface current slot-switch lock truth in `baseline-status` and `live-status`.
- [x] Ensure missing or malformed `state.env` does not emit raw race noise as the only signal.

## Slice 4: Verify and write back

- [x] Add focused regression tests for stale cleanup, active timeout, and observability.
- [x] Add the issue-bound implementation decision note.
- [x] Run targeted tests and `./bin/governance-check`.
