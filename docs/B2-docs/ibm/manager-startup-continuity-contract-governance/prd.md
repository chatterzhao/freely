# PRD: manager-startup-continuity-contract-governance

## Problem

Freely now has authoritative startup identity truth, but manager startup still lacks a canonical handoff contract. The runtime knows the expected continuity path yet treats continuity as prompt-only best effort during startup and as stop-time repair during failure, which leaves the outer loop without a reliable first artifact on the normal path.

## Product Requirement

1. Startup semantics must distinguish `launch bootstrapped` from `manager handoff materialized`.
2. The first manager handoff artifact must be bound to the launch and appear on the normal startup path.
3. The first implementation should minimize churn by reusing the existing expected continuity path and fallback writer seam.
4. Runtime status must expose handoff truth in a machine-readable way without immediately redefining daemon readiness.
5. Stop fallback must remain visibly repair-only.

## Acceptance

1. Canonical docs define the two-layer startup model and the normal-path handoff requirement.
2. Canonical docs select `runtime-seeded continuity claim/stub -> manager enrich` as the preferred initial implementation shape.
3. Canonical docs require a `manager_handoff_state`-style status surface distinct from authority/readiness truth.
4. Canonical docs keep `daemon start` readiness and startup authority repairs scoped out of this owner.
5. The packet lands as documentation-only owner truth on `develop`.
