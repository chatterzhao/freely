# Progress: cli-help-and-dry-run-contract-followthrough-governance

- issue_id: `I-20260405-2358-D`
- issue_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- title: `CLI help and dry-run contract followthrough governance`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/cli-help-dry-run-contract-followthrough-20260406-0408`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0408-feature-cli-help-dry-run-contract-followthrough`
- updated_at: `2026-04-06`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical CLI replay proved the remaining gap is a first-hop contract lane, not a runtime-control-plane lane.
- The bounded implementation target is explicit help semantics for the audited scripts plus a stable machine-readable dry-run result for `ai switch codex`.
- Fresh-project bootstrap, baseline/status scoping, and runtime supervision remain out of scope.

## Planned Verification

- `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
- `./bin/governance-check`
- `git diff --check`

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
- `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `bash docs/system/workspace/scripts/tests/test-merge-guarded`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `./bin/ai --quiet --format json --dry-run switch codex`
- `python3` JSON parse replay for `./bin/ai --quiet --format json --dry-run switch codex`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0408-feature-cli-help-dry-run-contract-followthrough --issue docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- `./bin/governance-check`
- `git diff --check`

## Next Action

- Commit this bounded owner in the dedicated feature worktree, then create the matching `test-pre-merge-*` batch for guarded promotion into `develop`.
