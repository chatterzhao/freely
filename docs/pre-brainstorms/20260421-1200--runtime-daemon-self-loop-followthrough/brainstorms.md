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
