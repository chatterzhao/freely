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
