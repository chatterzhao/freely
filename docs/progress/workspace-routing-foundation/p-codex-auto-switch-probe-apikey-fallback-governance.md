# Progress: codex-auto-switch-probe-apikey-fallback-governance

- issue_id: `I-20260407-0023-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- title: `Codex auto switch probe apikey fallback governance`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/codex-auto-switch-probe-apikey-fallback-20260406-2138`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback`
- updated_at: `2026-04-07`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Dogfooding exposed a remaining gap in no-arg `switch codex` and shared watchdog probing: `all_unavailable:*` from the account OAuth sweep stopped execution before saved apikey slots were exec-probed.
- This lane keeps the repair narrow to the completed Codex bundle/probe lineage without reopening broader IBM scope.
- Commit `eb709ea` carries the runtime fix plus the new regression that reproduces and locks the fallback behavior.

## Planned Verification

- `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-all-unavailable-falls-back-to-exec`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
- `./bin/governance-check`
- `git diff --check`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback --issue docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`

## Next Action

- Write the feature-worktree verification artifact, then create the fresh `test-pre-merge-*` batch for guarded promotion into `develop`.
