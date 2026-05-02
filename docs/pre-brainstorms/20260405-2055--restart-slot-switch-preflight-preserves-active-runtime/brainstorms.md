# Brainstorm - 20260405-2055--restart-slot-switch-preflight-preserves-active-runtime

## Problem

Canonical `develop` already froze startup-time slot-switch preflight for `freely start`, but `freely restart` still stops the current project runtime before discovering that a shared active codex slot-switch lock would block the next launch.

## Observed Runtime Facts

- `I-20260404-2148-A` completed a narrow owner for `freely start` plus lock observability on `doctor` and status surfaces.
- `I-20260327-2006-A` completed the parent project-command taxonomy and explicitly says future command-semantics changes must open a new lifecycle instead of reopening that owner.
- The current restart follow-on diff adds slot-switch preflight ahead of `stop_project_runtime` and proves, with a dedicated integration test, that an active shared lock must not tear down the already-running project runtime.
- The same lane also hardens adjacent runtime behavior that the restart path depends on: project-root cwd anchoring for relaunch helpers, stop-before-launch exit checks, tighter readiness polling, and atomic session-state writes.

## Routing Judgment

- This is a new follow-on owner on `workspace-routing-foundation`.
- It should depend on the completed startup preflight owner rather than widening it after completion.
- It should also inherit the completed project-command taxonomy rather than reopening that parent.
- The owner boundary should stay narrow: `restart` must preflight shared slot-switch state before stop, and a blocked restart must preserve the currently healthy project runtime.
