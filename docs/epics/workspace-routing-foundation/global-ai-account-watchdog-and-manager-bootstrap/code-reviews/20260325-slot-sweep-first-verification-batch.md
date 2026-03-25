# Code Review: global-ai-account-watchdog-and-manager-bootstrap

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

## Remaining Acceptance

- Manager needs to absorb this verified continuation and decide merge judgement for the dedicated worktree.
- After merge, `develop` replay still has to confirm the runtime uses the new slot-sweep-first path under canonical supervision.
