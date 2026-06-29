# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

## Result

- slot-sweep-first continuation passed focused verification in dedicated feature worktree

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive`
- `./bin/governance-check`

## What Changed

1. `availability-watchdog.sh` no longer treats cooldown or earliest-reset as the primary recovery gate for manager bootstrap.
2. `ensure_codex_slot_ready_for_manager()` now probes the current slot first and then does a full saved-slot sweep before deciding whether manager bootstrap may proceed.
3. `probe_all_codex_slots_and_update_cooldown()` now restores the original auth file and active slot when every saved slot is currently unusable, so a failed probe does not leave an invalid auth file in the real Codex working position.
4. `freely ai switch codex` automatic mode now switches only to a slot that passed a real probe; `all_unavailable` returns debug information without forcing the earliest-reset slot into the live Codex auth position.
5. Focused tests were rewritten to assert the slot-sweep-first contract directly rather than the older cooldown-driven wait path.

## Notes

- This batch absorbs the `20260325-0525` pre-brainstorm contract rewrite as same-family continuation under `I-20260318-1630`; it is not a parallel issue.
- The current gate is still feature-worktree verification plus manager merge judgement. This worktree is not `completed` yet.
- 2026-03-26 closeout audit rechecked fleet truth and merge position before declaring closure:
  - authoritative fleet truth is now a 12-worktree inventory from `git worktree list --porcelain`, cross-checked by `./bin/wt-status-all` and relevant worktree `git status`, and the latest stable recheck has moved again to `Summary: total=12, dirty=1`
  - the older continuity 5-tree / 7-tree / 10-tree snapshots, the older prompt-injected 6-tree / 9-tree fleet snapshots, and the 04:47 PDT `dirty=3` closeout note are stale history, not current cleanup truth
  - this replay owner is currently `ahead 162 / behind 12` relative to latest `develop`, so the verified batch is review-ready but not yet promote-closed
  - `feature/manager-scheduler-capacity-candidate-replay-20260324` remains frozen as `needs_research / retained-with-reason`, and is now clean again; its blocker remains canonical `develop` proof writeback, not replay-owner-local evidence
  - `feature/intake-absorption-closure-governance-20260326` is clean and sits `develop...HEAD = 3/0`, but canonical docs still lack explicit owner/phase absorption for it, so it remains `supervision-needed`
  - two additional 20260326 watchdog-related feature worktrees are now visible in the fleet and already absorbed by `develop`, but their dispositions differ: `feature/watchdog-auth-failure-control-plane-recovery-20260326` is still `ownership-followthrough-needed`, while `feature/watchdog-live-status-and-dispatcher-ready-20260326` is `cleanup-followthrough-needed`
  - `feature/latest-manager-continuity-worker-consumption-reconcile-20260326` remains an unresolved verification/cleanup followthrough lane and currently sits `develop...HEAD = 11/0`
  - three other 20260326 watchdog-related clean trees remain `supervision-needed`: `feature/watchdog-probe-early-deactivated-workspace-detect-20260326`, `feature/watchdog-slot-switch-global-launch-gate-20260326`, and `feature/watchdog-switch-stability-and-probe-freeze-20260326` still lack canonical owner/phase binding, and now sit `develop...HEAD = 1/1`, `5/0`, and `6/1`
  - `freely live-status --project ...` reports `pending_delegated_continuation_ids=none`, so the closeout lane stays manager-owned in the current worktree instead of emitting a new worker prompt

## Remaining Acceptance

- Manager needs to absorb this verified continuation and decide merge judgement for the dedicated worktree.
- After manager judgement, the branch still has to absorb latest `develop`, replay onto canonical `develop`, and confirm the runtime uses the new slot-sweep-first path under canonical supervision.
- The 2026-03-25 23:41 PDT develop-side `402 Payment Required` / `deactivated_workspace` cycle remains relevant as historical evidence for why this replay owner had to broaden auth-failure and no-launch handling, but it is no longer the primary closeout blocker after the 2026-03-26 canonical proof wave and latest manager-continuity worker-consumption repair.
- Cleanup / retirement remains closed until canonical `develop` completion verification exists.
