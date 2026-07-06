# PRD: manager-startup-continuity-materialization-governance

## Problem

Freely now knows when a launch is bootstrapped, and it knows where the first manager continuity file should live, but it still allows the normal startup path to proceed without materializing that file. This breaks Freely's own outer-loop expectations: the runtime can claim startup success while the first handoff artifact still depends on later manager behavior or stop-time repair.

## Product Requirement

1. The normal startup path must materialize the first manager continuity artifact at the prompt-required path.
2. The runtime-written startup artifact must remain distinguishable from stop fallback repair and from manager-written continuity.
3. Runtime status must expose machine-readable manager handoff state.
4. The first implementation must reuse the existing continuity-path seam and keep `daemon start` readiness unchanged.

## Acceptance

1. Startup writes a launch-bound continuity stub when the expected continuity file is missing.
2. Status can tell whether continuity is still missing, was startup-seeded, was repair-written on cleanup, or was materialized by the manager.
3. `live-status` and `fleet-status` surface this handoff state without regressing current continuity-gap visibility.
4. Focused regressions plus bounded runtime validation prove the new behavior.
