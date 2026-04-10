# Progress: preferred-auth-method-account-switch-fix

- issue_id: `I-20260410-1430-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/preferred-auth-method-account-switch-fix.md`
- title: `Fix preferred_auth_method lost when switching to account slot`
- phase_state: `done_ibm`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/preferred-auth-method-account-switch-fix-20260410-143000`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260410-143000-feature-preferred-auth-method-account-switch-fix`
- updated_at: `2026-04-10`
- follow_on_to: `I-20260405-0027-A`

## Summary

Narrow bug fix for `preferred_auth_method` field being lost when switching to account slot. Added fallback logic to set the field based on `slot_kind` when fragment doesn't provide it.

## Implementation

- Modified `codex_apply_saved_slot_config_fragment` in `ai-cli` to add slot-kind-aware fallback
- Added test assertion in `test-ai-cli-codex-apikey-slot-bundle-switch`

## Verification Evidence

- `test-ai-cli-codex-apikey-slot-bundle-switch` passes
- Git commit `358182bb` on feature branch

## Next Action

Merge to `develop` through `test-pre-merge-20260410-preferred-auth-fix`.
