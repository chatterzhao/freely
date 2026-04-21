# Tasks: runtime-daemon-self-loop-followthrough-governance

- [x] Reproduce the self-loop blocker on real Freely runtime behavior and isolate it to control-plane ownership rather than task-selection logic.
- [x] Ignore orphaned dispatcher/watchdog residue in user-facing repeated-start precheck when no authoritative supervisor exists.
- [x] Ignore unexpected daemon `TERM` without `stop.marker` while preserving explicit daemon stop semantics.
- [x] Add focused regressions for both seams and rerun nearby daemon/live-status coverage.
- [x] Materialize the candidate -> issue -> progress -> pre-tests -> review owner chain required for guarded promote.
- [x] Replay `feature/runtime-daemon-self-loop-blocker-20260421 -> test-pre-merge-20260421-runtime-self-loop-blocker` through `./bin/merge-guarded` and rerun owner gates on the protected test lane.
- [x] Keep canonical develop self-host acceptance and temporary lane retirement as post-promote completion conditions owned by the same issue, not as unfinished pre-promote task checklist items.
