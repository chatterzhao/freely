# Tasks: runtime-daemon-self-loop-followthrough-governance

- [x] Reproduce the self-loop blocker on real Freely runtime behavior and isolate it to control-plane ownership rather than task-selection logic.
- [x] Ignore orphaned dispatcher/watchdog residue in user-facing repeated-start precheck when no authoritative supervisor exists.
- [x] Ignore unexpected daemon `TERM` without `stop.marker` while preserving explicit daemon stop semantics.
- [x] Add focused regressions for both seams and rerun nearby daemon/live-status coverage.
- [ ] Replay the guarded `feature/* -> test-pre-merge-* -> develop` promotion with a lawful owner chain.
- [ ] On canonical `develop`, keep `freely daemon start` running until it finishes one task to the current-project success standard, closes the worktree, and proceeds to another task.
- [ ] Retire the temporary blocker worktree and disposable test-pre-merge branch after canonical develop absorbs the fix.
