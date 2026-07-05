# Brainstorms - 20260419-1630--runtime-startup-self-healing-boundary

- date: `2026-04-19`
- status: `pre-brainstorm`
- source: `real runtime replay on protected root`

## Context

Today the protected-root runtime was started from `/Users/zhaoyu/Downloads/code/my-freely/freely` with `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, then observed after roughly one minute through `live-status`, pid files, logs, and run-dir artifacts.

The current shape is not a normal manager-owned recovery:

1. `live-status` still reports `desired_runtime_state: running`, `last_supervisor_state: up`, and `last_exit_reason: starting`, but `activity_state` is already `stalled_without_runtime`.
2. `.freely/run/supervisor.pid` and `.freely/run/interruption-dispatch.pid` still exist, while `ps` no longer finds those processes.
3. startup traces stop at `A-L001 start_requested` and `A-L010 supervisor_started`; the AI loop never reaches a healthy handoff.
4. prompt / continuity artifacts still reference the missing worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-manager-startup-blocker-rootcause`.
5. `daemon-launch.log` already contains restart-storm and launch-failure evidence such as `fork: Resource temporarily unavailable` and `ai process exited rc=1`.

This means startup truth is already stale before a manager AI can lawfully take over. The system still exposes machine-owned runtime state that claims "up" while the actual processes and some referenced worktrees are gone.

## Why Existing Owners Do Not Fully Absorb This

Existing owners already cover adjacent seams, but not this exact boundary:

1. `runtime-selfhost-continuity-gap-and-status-truth-governance` is closed and was about surfacing bounded continuity/status truth, not repairing startup-time stale machine state before manager launch.
2. `freely-start-auto-recovery-rootcause-governance` is about after-failure recovery handoff once startup already has a lawful recovery owner.
3. the older daemon blocker thread referenced by current prompts points to a deleted worktree, which proves the present startup source-of-truth can rot before the AI loop has a chance to continue it.

So the missing owner is earlier and narrower: startup must canonicalize machine-owned truth before manager routing is allowed to treat the project as an AI-owned continuation.

## Proposed Boundary

Freeze one explicit split:

1. `runtime-owned startup self-heal`
   - validate pid files against real processes
   - validate referenced worktree / branch / continuity / prompt artifacts against current disk truth
   - clear or downgrade obviously stale machine-owned state
   - if something cannot be repaired safely, publish machine-readable blocked truth instead of pretending runtime is up
2. `manager-owned recovery after launch`
   - read the canonicalized startup truth
   - decide continuation, recovery, re-materialization, or fresh doc-loop routing
   - absorb stale delegated work only after runtime has stopped lying about its own liveness and anchors

## Machine-Owned Self-Heal Scope

Startup should be allowed to repair only facts that scripts can prove locally:

1. stale pid files whose processes are gone
2. `desired_runtime_state=running` plus dead supervisor / dispatcher process combinations
3. stale startup locks or dispatcher references whose owners no longer exist
4. continuity / prompt / state references that point to missing files
5. continuity / prompt / handoff references that point to missing worktree directories
6. non-canonical or no-longer-existing worktree anchors that block lawful routing

For these cases, runtime should either:

1. heal the state automatically when the proof is deterministic, or
2. publish a bounded blocked / degraded startup truth for the manager instead of inventing a healthy runtime.

## Not Runtime-Owned

Startup self-heal should not silently decide higher-order governance questions:

1. whether an old continuation should be retired, revived, or split into a new owner
2. whether a stale worktree reference should reopen an old issue or spawn a new worktree
3. whether delegated human interruptions should be reclassified, dropped, or promoted
4. any code / milestone / doc-loop judgment that requires semantic interpretation rather than local proof

Those belong to the manager only after startup truth is canonical.

## Success Criteria For This Research Slice

This pre-brainstorm is complete only if it freezes the following:

1. the observed protected-root failure shape and evidence sources
2. the precise handoff line between runtime-owned startup self-heal and manager-owned recovery
3. a concrete list of state classes that startup may auto-heal versus must surface as blocked truth
4. why this is not already absorbed by the closed status-truth owner or the in-flight after-failure recovery owner

## Next Question

If this boundary remains stable, the next owner should likely materialize a bounded startup-governance issue that adds pre-launch canonicalization and focused tests for stale pid, missing worktree anchor, and missing continuity / prompt references.
