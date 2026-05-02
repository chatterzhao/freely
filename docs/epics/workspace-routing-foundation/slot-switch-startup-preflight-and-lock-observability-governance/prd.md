# PRD: slot-switch-startup-preflight-and-lock-observability-governance

## Goal

Make Freely startup and observability truthful when a shared codex slot-switch lock is present, stale, or ambiguous.

## Why Now

Dogfooding on 2026-04-04 proved both that a stale shared lock can block startup and that the latest failures can already be caused by something else (`auth_failure`). Operators currently have to infer too much from indirect logs and manual filesystem inspection, so startup governance is still underspecified.

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
- `docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
- `docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/*.md`

## Non-Goals

- Do not absorb websocket permission-denied blocked-intake governance.
- Do not change global slot/account recovery ownership beyond the startup/status truth required here.
- Do not add force-delete behavior for active shared locks.

## Non-Negotiables

- stale cleanup requires a missing or dead `owner_pid`
- active lock must remain shared/global and therefore non-destructively handled
- startup and observability must share the same lock-state taxonomy
- develop-bound runtime edits must be backed by an issue-bound implementation decision note

## Decomposition Tree

1. materialize issue and progress truth
2. implement shared lock snapshot helpers for startup/status/doctor
3. add focused regressions for stale, active, and observability cases
4. run governance and targeted runtime verification

## Eval Plan

### Startup stale-lock recovery

- environment: feature worktree
- evidence: `freely start` clears a stale shared lock and proceeds
- failure signal: manual lock deletion is still required

### Active-lock bounded failure

- environment: feature worktree
- evidence: `freely start` times out or defers clearly while the live lock owner is still running
- failure signal: startup silently hangs, force-removes the live lock, or emits only raw shell noise

### Observability truth

- environment: feature worktree
- evidence: `doctor` and status output show current structured lock state
- failure signal: current lock state is invisible or only appears as raw stderr
