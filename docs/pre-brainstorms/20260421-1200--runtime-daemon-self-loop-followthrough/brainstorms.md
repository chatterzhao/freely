# Brainstorms - 20260421-1200--runtime-daemon-self-loop-followthrough

## Context

Canonical `develop` already contains the broader runtime and three-loop architecture owners, but dogfooding on `2026-04-21` exposed one still-open operational blocker:

- `freely daemon start` could complete one manager patrol round and then stop progressing because the runtime was vulnerable to being recorded as `operator_stop` from an unexpected daemon-side `TERM`
- after a stop or inconsistent state, a lone interruption dispatcher/watchdog residue could also make the next user-facing `start` or `daemon start` falsely refuse with `already running`

This is not a new architecture lane. It is a narrow followthrough owner for a real self-host runtime blocker that prevents Freely from continuing its own task loop.

## Decision

Materialize a bounded followthrough owner that:

1. fixes the daemon self-loop blocker,
2. carries the required candidate -> issue -> progress -> pre-tests -> review evidence for guarded promotion,
3. proves the final acceptance surface on canonical `develop`: Freely can self-start, select a task, complete it to the current-project success standard, close the worktree, and continue to the next task.

## Boundaries

- do not widen into a generic scan architecture redesign
- do not reopen unrelated runtime, watchdog, or live-status owners
- do not weaken Freely's freedom of action while optimizing control-plane behavior
- retire the temporary blocker worktree and disposable test-pre-merge branch after canonical `develop` absorbs the fix

## Followthrough Update

Guarded replay on canonical `develop` exposed two more same-family runtime seams without changing the owner boundary:

1. manager continuity had already selected worker prompts, yet runtime did not parse the current `## Worker Delegation` handoff shape into launchable prompt paths, so autonomous looping stalled before worker execution;
2. after that parser repair, runtime could still misclassify an already merged-clean blocker worktree as a recoverable active worker instead of routing it toward cleanup followthrough retirement.

The bounded response stays the same: keep runtime truth aligned with current manager-written continuity, treat `merged-clean` / `retire-ready` worktrees as manager-owned cleanup targets rather than edit lanes to auto-recover, and prove the result on canonical `develop` through real self-work completion plus lawful worktree closeout.
