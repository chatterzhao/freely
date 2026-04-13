# PRD: runtime-startup-authority-and-readiness-governance

## Goal

Make Freely runtime startup authoritative: one current launch identity, one bounded startup publication phase, one ready definition that both foreground and daemon entrypoints can trust.

## Why Now

Recent dogfood evidence shows that current `develop` can still:

1. accept a fake argv process as a valid supervisor
2. release the project start lock before startup truth is durably published
3. let `daemon start` report ready on PID resemblance alone
4. preserve stop markers based on ghost same-project supervisors

These are not independent bugs. They are all consequences of a missing authoritative launch model.

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
- `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- new fake-supervisor rejection regression
- new launch-truth or daemon-ready regression
- `./bin/freely live-status`
- `./bin/freely fleet-status`

## Non-Goals

- No manager continuity contract redesign in this owner
- No command-surface rename or foreground/daemon semantics rewrite
- No generic process-policy redesign beyond what current-launch authority requires
- No attempt to close every recovery problem in the runtime family

## Non-Negotiables

- startup truth must be runtime-owned, not argv-owned
- later starters must not reason against a half-published launch
- daemon ready must prove current-launch truth, not just a surviving PID
- stop cleanup must only trust validated launch ownership
- the closeout gate must include a real-repo-shaped replay, not only synthetic tests

## Prototype Path

1. Introduce a current-launch identity or truth artifact.
2. Publish startup truth before later starters may classify the launch as attachable or repairable.
3. Move daemon-ready checks onto current-launch truth.
4. Reduce process discovery to diagnostics or stale-process hints.
5. Replay real-repo foreground and daemon bounded starts against the new authority model.

## Eval Plan

Success:

- fake supervisors are rejected
- same-project startup produces one authoritative launch
- daemon ready tracks current-launch truth
- stop cleanup no longer preserves ghost stop state
- real-repo replay agrees with the synthetic regressions

Failure:

- daemon ready still succeeds on PID resemblance alone
- the start lock still releases before authoritative startup publication
- fake argv processes still pass validation
- the implementation solves synthetic tests but not the real dogfood replay

## Dev-Loop Handoff

Keep the implementation narrow: repair launch identity and readiness first, then hand the resulting phase model to the future manager-continuity contract owner.
