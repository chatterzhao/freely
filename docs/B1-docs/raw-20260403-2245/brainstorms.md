# Brainstorms - 20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state

## Context

Today the canonical `develop` cleanup flow hit a real sandbox boundary that the current Freely runtime contract does not yet absorb cleanly.

Observed failures in a sibling feature worktree:

1. `git add` in the worktree failed because the current tool sandbox denied writes to `.git/worktrees/.../index.lock`.
2. Falling back to Freely runtime did not fully recover the path:
   - `freely start` with the default global state root failed because it tried to write `~/.freely/projects.*`, which was outside the current sandbox.
   - forcing `FREELY_HOME` into a project-local writable path got past that first failure, but runtime bootstrap still failed because readiness / discovery logic hard-depends on `/bin/ps`, which is also denied in the same sandbox.

The result is a concrete dogfood gap:

- the current session cannot safely commit the salvage worktree changes itself
- the sanctioned Freely runtime path also cannot fully take over inside the same restricted environment

That means the system still lacks a canonical sandbox-compatible route for protected-root supervision plus sibling-worktree owner continuation.

## Why This Is A New Follow-On

This should not be silently absorbed into already-completed owners:

1. `I-20260403-2041-A` closed sibling worktree tool-boundary bootstrap, but not runtime operator-state durability or process-discovery degradation under sandboxed operator sessions.
2. `I-20260327-2006-A` closed project command semantics and explicit restore-work taxonomy; that parent explicitly says future command/runtime contract changes must open a new lifecycle.
3. `global restart restore memory` already froze the shared/global restart manifest under `$FREELY_HOME`, but did not answer what happens when the current operator session cannot write the default global home at all.

So the remaining question is narrower and different:

- how should Freely bootstrap or degrade operator state when the current sandbox cannot reach the default global control-plane home or process-inspection binaries

## Problem

Freely currently depends on two assumptions that are not always true inside sandboxed operator sessions:

1. global operator state under `$FREELY_HOME` is writable
2. runtime discovery/readiness can rely on `/bin/ps`

If either assumption fails, a lawful recovery path can disappear:

- direct worktree Git writes are blocked
- protected root remains intentionally non-authoritative for owner development
- runtime takeover also fails before it can delegate or continue the correct worktree

That is exactly the kind of drift that tempts agents or users back toward editing the wrong branch or bypassing the managed control plane.

## Boundary

Keep this follow-on narrow:

1. sandbox-compatible bootstrap for Freely operator/global state
2. lawful fallback when default `$FREELY_HOME` is unavailable to the current session
3. readiness/discovery degradation when `/bin/ps` or equivalent process inspection is blocked
4. documentation and tests that make the sandbox-compatible route explicit

Do not absorb:

1. another broad tool-boundary redesign
2. generic Git sandbox bypass
3. unrelated restart/global restore redesign
4. reopening completed project-command taxonomy or tool-materialization umbrellas

## Proposed Direction

Promote a narrow owner that decides and proves:

1. whether Freely should automatically fall back to a project-local or project-managed operator-state root when the default `$FREELY_HOME` is unwritable
2. which operator artifacts must remain global/shared versus which may lawfully degrade into project-scoped bootstrap state
3. how runtime bootstrap/readiness behaves when process-inspection binaries are sandbox-blocked
4. how `freely start/status/live-status/chat` should surface this degraded mode without pretending the runtime is healthy

## Current Judgement

This is worth a dedicated lifecycle because it exposed a real operational dead-end during canonical cleanup:

- direct Git ownership actions were sandbox-blocked
- the sanctioned runtime path was also partially blocked
- the remaining gap is concrete, reproducible, and tightly scoped

If Freely does not absorb this explicitly, the claimed safe path back out of protected-root drift still has a hidden failure mode.
