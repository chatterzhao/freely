# IBM Brainstorm: slot-switch-startup-preflight-and-lock-observability-governance

## Goal

Freeze the narrow issue-level contract for startup preflight and lock observability before implementation broadens into unrelated supervision failure families.

## Decision

1. The owner remains startup-scoped: `freely start`, `doctor`, and status truth.
2. Stale lock cleanup is lawful only when the recorded `owner_pid` is absent or dead.
3. Active shared lock is never force-removed by a project-local start path.
4. `state.env` races or corruption must be surfaced as structured degraded truth, not raw shell noise.

## Implementation Route

1. Add shared helper logic in `runtime/freely` for current shared lock snapshot.
2. Run that helper as startup preflight before supervisor bootstrap.
3. Reuse the same snapshot when printing status or doctor output.
4. Add focused regression tests that pin stale cleanup, active timeout, and status visibility.
