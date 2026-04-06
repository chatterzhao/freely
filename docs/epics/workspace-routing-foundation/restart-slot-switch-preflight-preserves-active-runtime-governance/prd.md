# PRD: restart-slot-switch-preflight-preserves-active-runtime-governance

## Goal

Make `freely restart` safe when a shared codex slot-switch lock would block the next launch, preserving the current project runtime instead of tearing it down first.

## Why Now

The completed startup-lock owner proved that shared lock state must be classified before launch, but restart still had a sequencing hole: a healthy current runtime could be sacrificed before that same bounded failure surfaced.

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
- `docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
- `docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`

## Non-Goals

- Do not redefine startup/status lock observability taxonomy.
- Do not redesign generic watchdog restart policy.
- Do not widen into standalone account-switch architecture or frontend control surfaces.

## Non-Negotiables

- restart preflight happens before `stop_project_runtime`
- active shared slot-switch lock never causes project-local destructive stop first
- preserved-runtime behavior must be proven by an end-to-end integration test with stable pid evidence
- restart-adjacent durability hardenings must stay bounded to behavior needed for this contract

## Decomposition Tree

1. materialize the follow-on owner and bind the feature lane
2. preflight restart before stop
3. harden the adjacent helper paths that make preserved restart truthful
4. replay focused regressions and record verification

## Eval Plan

### Restart blocked by active shared lock

- environment: feature worktree
- evidence: `freely restart` fails behind active shared lock while existing supervisor/AI pids stay alive
- failure signal: restart stops the current runtime before surfacing the lock failure

### Command ordering

- environment: feature worktree
- evidence: `cmd_restart` calls preflight before stop/start and aborts early on preflight failure
- failure signal: restart still reaches stop/start on preflight failure

### Restart-adjacent durability

- environment: feature worktree
- evidence: session rotation, checkpoint, and account-switch regressions still pass after the helper hardenings
- failure signal: adjacent runtime tests start flaking or regress
