# PRD: runtime-start-stop-lifecycle-and-process-leak-governance

## Goal

Make Freely start/stop semantics CLI-first and leak-resistant so repeated user starts reject lawfully, stop converges on same-project runtime processes, and local AI runtime failures do not relaunch through stale process leftovers.

## Product requirements

1. `freely start` and `freely daemon start` must reject repeated user launches when an authoritative same-project runtime is already active.
2. `--force` must remain explicit stop-then-start rather than hidden attach or repair.
3. Same-project startup lock truth must be published and cleaned so lawful retries can distinguish self-owned, stale, and failed-start cases.
4. `freely stop --project` must terminate discovered same-project watchdog and interruption-dispatcher processes that could otherwise relaunch the runtime.
5. `monitor-ai-cli.sh` must classify local `.iflow` state failures as runtime failures and terminate the AI descendant tree.
6. Lifecycle-trace and interruption-manager evidence must remain compatible with the bounded contract.

## Out of scope

1. manager continuity or handoff-state redesign
2. generic slot recovery or auth recovery policy
3. a broader runtime process-manager rewrite beyond the bounded same-project leak seam
4. new protected-root development paths outside the guarded merge lifecycle
