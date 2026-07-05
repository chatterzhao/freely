# Issue: slot-switch-startup-preflight-and-lock-observability-governance

- issue_id: `I-20260404-2148-A`
- title: Slot-switch startup preflight and lock observability governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `slot-switch-startup-preflight-and-lock-observability-governance`
- issue-name: `slot-switch-startup-preflight-and-lock-observability-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260404/candidates.md#c-20260404-2148-a`
- source_brainstorm: `docs/B1-docs/raw-20260404/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-slot-switch-startup-preflight-and-lock-observability-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews`
- depends_on: `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` has already shown two distinct truths on 2026-04-04:

1. a stale shared `~/.codex/slot-switch.lock` could block `freely start` until an operator manually removed it
2. the latest repeated root startup failures are no longer caused by a current lock and now exit with `auth_failure`

That combination means the immediate operator diagnosis is currently too implicit. Lower-layer launchers already contain partial stale-cleanup and bounded-wait behavior, but Freely still lacks a governed startup preflight plus a structured truth surface that explains whether the current lock state is `idle`, `active`, `stale`, or `ambiguous`.

## Scope

1. Add a startup preflight for shared codex slot-switch lock state before Freely commits to a fresh project runtime launch.
2. Keep stale cleanup narrowly bounded to the cases where the lock owner PID is missing or dead.
3. Surface current slot-switch lock truth through `freely start`, `doctor`, and status output without leaking raw shell-race noise as the only signal.
4. Add focused regression tests for stale-lock cleanup, active-lock timeout/defer behavior, and structured status/doctor visibility.

## Non-Goals

1. Do not widen this owner into websocket blocked-intake supervision or generic manager continuity failures.
2. Do not reopen completed owners such as `I-20260318-1630` or `I-20260327-2006-A`.
3. Do not allow project-local force removal of a live shared lock.
4. Do not redesign global account watchdog semantics beyond the minimum startup/status contract needed here.

## Acceptance

1. `freely start` classifies current slot-switch lock state before launch and handles `stale` versus `active` differently.
2. A stale shared lock with a dead or missing `owner_pid` is cleaned automatically and startup proceeds without requiring manual filesystem deletion.
3. An active shared lock causes bounded wait and then a clear failure/defer path instead of a silent hang or ambiguous stderr.
4. `doctor` and at least one status surface expose structured current slot-switch lock truth.
5. Missing or malformed `state.env` no longer degrades into raw `sed` noise as the only operator-visible explanation.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
- `bash docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
- `bash docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-status-family`
- `./bin/governance-check`

## Completion

- `docs/B1-docs/raw-20260404/brainstorms.md`
- `docs/B1-docs/raw-20260404/candidates.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/brainstorms/b-slot-switch-startup-preflight-and-lock-observability-governance.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-verification.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-canonical-closeout-verification.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/prd.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-slot-switch-startup-preflight-and-lock-observability-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
- `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
- `docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
- `docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`

## Next

- Completed on canonical `develop` via merge `9fa8ec3`.
- The missing protected-merge receipt for `9fa8ec3` was repaired through the ordinary backfill ledger instead of widening runtime scope or rewriting history.
- Reopen only if canonical `develop` regresses the startup-lock contract itself; persistent `auth_failure` remains separate follow-on evidence.
