# Brainstorm: manager-startup-continuity-materialization-governance

## Goal

Turn the frozen manager startup contract into the smallest executable runtime slice that restores a real first handoff artifact on the normal startup path.

## Root Cause

1. Startup authority fixed launch truth, but it intentionally stopped at `launch_bootstrapped`.
2. The runtime already knows the expected continuity path when it assembles the manager prompt.
3. Normal startup still treated "prompt written and AI launched" as good enough, even when the prompt-required continuity file did not yet exist.
4. The only built-in writer for that continuity path lived in stop fallback, so a repair mechanism was accidentally carrying part of the normal-path contract.

## Chosen Implementation Shape

1. Build the prompt and resolve the expected manager continuity path.
2. If the prompt-required continuity file is absent, runtime seeds a launch-bound startup stub at that path before AI launch.
3. Classify the observed artifact by writer so status can distinguish:
   - `missing`
   - `seeded_stub`
   - `repair_fallback`
   - `materialized`
4. Expose the classification through `live-status` and `fleet-status`.

## Rejected Alternatives

1. Make `daemon start` block on manager continuity in this same lane.
2. Keep treating stop fallback as acceptable normal startup evidence.
3. Invent a new sidecar artifact family instead of using the prompt-required continuity path.
4. Delay status surfacing until after full manager enrichment exists.

## Guardrails

1. The startup stub exists to materialize the first handoff seam, not to replace manager-written continuity.
2. Status must make repair fallback visibly different from normal startup seeding.
3. This owner does not define a timeout or SLA for how long `seeded_stub` may persist.
4. This owner does not reopen startup authority or broaden the runtime state machine.
