# Verification: runtime-startup-self-healing-governance disabled slot auto-switch continuation

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- verification_date: `2026-04-23`
- branch: `feature/guard-disable-slot-switch-probe`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-guard-disable-slot-switch-probe`
- verifier: `codex`

## Why This Continuation Exists

An operator report on `2026-04-23` showed a narrower residual defect inside the same owner boundary: even with `AUTO_SWITCH_TOOL=false` and `AUTO_SWITCH_SLOT=false`, background startup/watchdog recovery could still inventory saved codex slots, probe them by switching live auth, and leave `~/.codex/auth.json` rewritten to an unusable slot. That violates this owner's explicit non-goal and acceptance contract around disabled auto-switch controls.

## Commands

1. Feature lane:
   - `bash docs/system/workspace/scripts/tests/test-freely-start-skips-preflight-slot-recovery-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-watchdog-manager-entry-skips-slot-selection-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-watchdog-probe-all-skips-sweep-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
2. Premerge lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260423-test-pre-merge-guard-disable-slot-switch-probe`:
   - `bash docs/system/workspace/scripts/tests/test-freely-start-skips-preflight-slot-recovery-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-watchdog-manager-entry-skips-slot-selection-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-watchdog-probe-all-skips-sweep-when-auto-switch-slot-disabled`
   - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`

## Results

1. `preflight_codex_slot_recovery_before_start_or_fail()` now returns before saved-slot selection when `AUTO_SWITCH_SLOT=false`, so startup preflight no longer inventories or switches codex slots under a disabled policy.
2. `availability-watchdog.sh` now centralizes the same boolean gate and blocks manager entry slot selection, full-sweep probing, and physical `switch_to_codex_slot()` execution when slot auto-switch is disabled.
3. The three new focused regressions all pass in both the feature lane and the guarded premerge lane, proving:
   - startup preflight does not enter saved-slot recovery,
   - watchdog manager entry does not select or switch a slot,
   - watchdog full-sweep probe short-circuits before enumerating slots, probing, or touching live auth.
4. `test-ai-cli-switch-default-tool` still passes in both lanes, so explicit human-invoked `ai switch` behavior remains intact while only background auto-recovery paths are blocked.

## Verdict

This continuation satisfies the still-open portion of the owner contract around disabled auto-switch controls: when `AUTO_SWITCH_SLOT=false`, runtime startup/watchdog recovery no longer rewrites `~/.codex/auth.json` behind the operator's back. The remaining closeout is canonical `develop` replay with the disabled setting to confirm the protected root now preserves live auth truth over time.

## Implementation Decision Note

- decision: `Treat AUTO_SWITCH_SLOT=false as a hard stop for startup/watchdog codex slot recovery by short-circuiting preflight, manager entry selection, full-sweep probing, and the physical slot-switch helper before they touch live auth material.`
- why_this: `The observed field defect was not that manual switch was wrong; it was that background recovery still traversed saved slots and rewrote ~/.codex/auth.json after the operator had explicitly disabled slot auto-switch. The narrowest correct repair is therefore to stop those auto-recovery entrypoints before any slot inventory, probe, or switch occurs.`
- alternatives_considered: `Only guard switch_to_codex_slot and let probes keep enumerating candidates; rely on auth-change-wake suppression alone; widen the repair into a broader account-runtime redesign; introduce a third config flag just for probing.`
- boundary_non_goals: `This continuation does not change explicit human-invoked ai switch behavior, does not redesign codex slot inventory semantics, does not widen into cross-tool recovery policy, and does not re-open broader auth-change lifecycle work outside this owner's disabled-auto-switch contract.`
- residual_risk: `Protected-root replay on canonical develop still needs to confirm no other background path outside startup/watchdog recovery mutates ~/.codex/auth.json while AUTO_SWITCH_SLOT=false. If that replay still changes live auth, the next seam is a remaining non-watchdog auto-recovery caller rather than the probe/switch helpers covered here.`
