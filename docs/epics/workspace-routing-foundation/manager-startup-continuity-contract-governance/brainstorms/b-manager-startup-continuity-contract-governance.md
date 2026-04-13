# Brainstorm: manager-startup-continuity-contract-governance

## Goal

Freeze the startup-handoff contract that should sit on top of authoritative launch truth without widening back into generic runtime redesign.

## Frozen Conclusions

1. `launch_bootstrapped` is not the same thing as `manager_handoff_materialized`.
2. The first handoff artifact belongs to the normal startup path, not to stop repair.
3. The narrowest first implementation seam is in `runtime/freely` after prompt assembly and before AI launch:
   - runtime already knows the expected continuity path from the prompt
   - runtime already has fallback continuity writing logic
   - the most economical next step is to seed a continuity claim/stub on the normal path and let manager enrich it
4. Status should expose a machine-readable manager handoff state, but the first contract freeze should not yet redefine `daemon start` readiness around manager continuity.

## Rejected Alternatives

1. Keep relying on prompt wording alone and treat missing continuity as a manager-quality issue.
2. Treat stop fallback as acceptable normal startup evidence.
3. Widen startup authority again and make `daemon start` wait for manager continuity before the handoff contract is even frozen.
4. Invent a brand-new sidecar artifact family before using the existing expected continuity path seam.

## Implementation Shape Chosen For Follow-On Owner

1. Build prompt and determine expected manager continuity path.
2. Runtime seeds a launch-bound continuity claim/stub at that path on the normal path.
3. Manager replaces or enriches that stub with semantic continuity content.
4. Runtime exposes `manager_handoff_state` separately from startup authority/readiness truth.
5. Stop fallback remains available only when the normal path failed to materialize valid continuity.

## Guardrails

1. This owner freezes contract and routing only.
2. It does not claim runtime behavior has already changed.
3. Follow-on implementation should stay bounded to the stub/state seam and not expand into unrelated worker-continuity or watchdog policy work.
