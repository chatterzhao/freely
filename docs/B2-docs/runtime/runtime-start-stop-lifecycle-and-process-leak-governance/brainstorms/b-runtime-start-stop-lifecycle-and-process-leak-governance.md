# Brainstorm: runtime-start-stop-lifecycle-and-process-leak-governance

- issue_id: `I-20260417-0445-A`
- date: `2026-04-18`
- source_candidate: `docs/B1-docs/raw-20260417/candidates.md#c-20260417-0445-a`

## Problem slice

The runtime defect has converged to one bounded implementation seam:

1. user-facing `freely start` and `freely daemon start` still drifted toward attach or repair semantics instead of a clear stop-first contract
2. startup and stop could race through stale project start-lock truth, leaving repeated start behavior ambiguous
3. same-project watchdog or dispatcher discovery relied too heavily on pid files, so `stop` could leave relaunch-capable processes alive
4. `monitor-ai-cli.sh` still needed runtime-failure classification and full process-tree cleanup to prevent local fast-exit storms from silently recreating the runtime
5. lifecycle tracing needed a durable contract so the bounded start/stop path can be debugged without reopening broader runtime governance

## Chosen shape

1. Reject repeated user-facing `freely start` and `freely daemon start` when an authoritative same-project runtime is already active.
2. Treat `--force` as explicit stop-then-start rather than implicit attach.
3. Publish and clean same-project startup lock truth so repeated starts, self-owned locks, and stale active locks are all handled lawfully.
4. Discover same-project watchdog and interruption-dispatcher processes authoritatively enough that `freely stop --project` converges to zero supervisor/watchdog/dispatcher/AI descendants within the bounded cleanup window.
5. Classify local `.iflow` state failures as runtime failures and terminate the whole AI descendant tree on failure.
6. Keep lifecycle-trace instrumentation and the three-loop trace contract limited to this bounded start/stop leak seam.

## Rejected shortcuts

1. Do not keep user CLI attach or repair as the default repeated-start contract.
2. Do not treat pid-file-only cleanup as sufficient proof that the runtime is fully stopped.
3. Do not widen this owner into manager continuity, slot recovery, or unrelated runtime orchestration policy.
4. Do not rely on a single kill of the direct AI pid when runtime failure can leave descendant processes alive.
