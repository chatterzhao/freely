# Progress: cli-wrapper-packaging-and-regression-surface-governance

- issue_id: `I-20260405-2358-C`
- issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- title: `CLI wrapper packaging and regression-surface governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/cli-command-audit-20260406-0015`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0015-feature-cli-command-audit`
- updated_at: `2026-04-06`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Full `bin/` command audit proved a bounded packaging/regression layer is still broken even when the underlying features exist.
- This owner is addressing the highest-leverage subset first: runnable wrapper executable bits, `freely ai --help` shell noise, and worktree-sensitive auth-change wake regression coverage.
- Project-target bootstrap/status drift and runtime control-plane instability remain explicitly out of scope for this lane.
- Canonical `develop` absorbed the lane through `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout` and guarded merge `8e0985b`, then passed focused post-merge command followthrough for the repaired surfaces.

## Verification Evidence

- `./bin/ai --help`
- `./bin/test-freely-fleet-status`
- `./bin/test-rust-toolchain-preflight`
- `./bin/test-ai-cli-login-triggers-auth-change-wake`
- `./bin/test-ai-cli-switch-triggers-auth-change-wake`
- `./bin/check-tauri-probe-host`
- `./bin/tauri-probe-dev`
- `git diff --check`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0035-test-pre-merge-cli-wrapper-regression-closeout --issue docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`

## Closure Evidence

- feature commits `f2c0ad1` and `3a5aff2`
- premerge merge `ab7a9b8`
- develop merge `8e0985b`
- `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`
- `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` regresses runnable wrapper packaging, `freely ai --help` cleanliness, or auth-change wake determinism.
- Keep project-target bootstrap/status drift and runtime control-plane findings in separate owners.
- Track the newly exposed `governance-check` ancestry-audit false positive as a separate pre-brainstorm instead of widening this packaging lane.
