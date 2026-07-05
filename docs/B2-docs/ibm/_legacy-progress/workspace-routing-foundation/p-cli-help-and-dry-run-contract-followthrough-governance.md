# Progress: cli-help-and-dry-run-contract-followthrough-governance

- issue_id: `I-20260405-2358-D`
- issue_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- title: `CLI help and dry-run contract followthrough governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0408-feature-cli-help-dry-run-contract-followthrough`
- updated_at: `2026-04-09`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical CLI replay proved the remaining gap is a first-hop contract lane, not a runtime-control-plane lane.
- The bounded implementation target is explicit help semantics for the audited scripts plus a stable machine-readable dry-run result for `ai switch codex`.
- Fresh-project bootstrap, baseline/status scoping, and runtime supervision remain out of scope.
- Canonical `develop` now carries the bounded owner through guarded merge `cb46eabf`, and a closeout replay on `2026-04-09` confirmed the help and dry-run contracts still hold on tracked root.

## Planned Verification

- `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
- `./bin/governance-check`
- `git diff --check`

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
- `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `./bin/ai --quiet --format json --dry-run switch codex`
- `python3` JSON parse replay for `./bin/ai --quiet --format json --dry-run switch codex`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0408-feature-cli-help-dry-run-contract-followthrough --issue docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- `./bin/governance-check`
- `git diff --check`
- `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260409-cli-help-and-dry-run-contract-followthrough-canonical-closeout-verification.md`

## Closure Evidence

- feature merge `4c87504a`
- develop merge `cb46eabf`
- `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`
- `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260409-cli-help-and-dry-run-contract-followthrough-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` regresses the explicit help contract or bounded dry-run JSON semantics.
