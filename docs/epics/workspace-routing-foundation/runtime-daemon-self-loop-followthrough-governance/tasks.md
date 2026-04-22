# Tasks: runtime-daemon-self-loop-followthrough-governance

- [x] Reproduce the self-loop blocker on real Freely runtime behavior and isolate it to control-plane ownership rather than task-selection logic.
- [x] Ignore orphaned dispatcher/watchdog residue in user-facing repeated-start precheck when no authoritative supervisor exists.
- [x] Ignore unexpected daemon `TERM` without `stop.marker` while preserving explicit daemon stop semantics.
- [x] Add focused regressions for both seams and rerun nearby daemon/live-status coverage.
- [x] Parse the current `## Worker Delegation` continuity shape into concrete runtime worker launches.
- [x] Settle merged-clean blocker worktrees toward cleanup followthrough retirement instead of runtime auto-recovery, and let cleanup reclaim stale recorded ownership for those lanes.
- [x] Materialize the candidate -> issue -> progress -> pre-tests -> review owner chain required for guarded promote.
- [x] Replay `feature/runtime-daemon-self-loop-blocker-20260421 -> test-pre-merge-20260421-runtime-self-loop-blocker` through `./bin/merge-guarded` and rerun owner gates on the protected test lane.
- [x] Keep canonical develop self-host acceptance and temporary lane retirement as post-promote completion conditions owned by the same issue, not as unfinished pre-promote task checklist items.
- [x] Enforce structured manager / worker exit contracts so runtime can stop, resume, or delegate from machine-checkable artifacts instead of inferring intent from free text.
- [x] Reuse the exact current role resume target when an exit contract artifact is missing or malformed, and block broader patrol until that same session repairs the contract.
- [x] Keep cleanup-governance handoff workers launchable when their prompt still carries full verification metadata and external cleanup scope, instead of auto-settling them as merged-lane retirement before the real cleanup work runs.
- [x] Keep reconnect-in-progress logs on the bounded execution-network retry path until the current tool actually exits, and restore the original tool after one fallback episode exhausts every configured fallback.
- [x] Keep exit-contract repair relaunches on the same resume path across supervisor restarts and same-process relaunch loops, so repair rounds do not regress into `initial_start`.
