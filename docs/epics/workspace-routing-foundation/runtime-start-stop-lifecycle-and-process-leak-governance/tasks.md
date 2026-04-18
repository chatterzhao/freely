# Tasks - runtime-start-stop-lifecycle-and-process-leak-governance

1. Reject repeated user-facing start and daemon-start when the same-project runtime is already active.
2. Publish and clean same-project startup lock truth across self-owned, stale, orphaned, and launch-failure cases.
3. Terminate discovered same-project watchdog and interruption-dispatcher processes during stop followthrough.
4. Treat local `.iflow` state failures as runtime failures and terminate the AI descendant tree.
5. Preserve bounded lifecycle-trace and interruption-manager regressions for the new contract.
6. Replay the focused regressions plus governance-check in `premerge-integration` before guarded promotion to `develop`.
