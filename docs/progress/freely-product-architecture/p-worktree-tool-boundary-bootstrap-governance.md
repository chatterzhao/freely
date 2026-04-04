# Progress: worktree-tool-boundary-bootstrap-governance

- issue_id: `I-20260403-2041-A`
- issue_path: `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
- title: `Worktree tool boundary bootstrap governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/tool-sandbox-worktree-bootstrap-20260403-204147`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-204147-feature-tool-sandbox-worktree-bootstrap`
- updated_at: `2026-04-03`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner is the narrow follow-on for the sibling-worktree gap left after the completed tool-materialization slice.
- `freely sync-tooling` is now the canonical rematerialization primitive for project-local tool boundaries.
- `wt-create` and protected-branch `post-checkout` auto-worktree creation now call that primitive, so ignored or untracked local tool directories do not strand the boundary contract in the project root.
- `tool-launchers.sh` now extends supported tool boundaries to the sibling worktrees root at launch time, while keeping the project root as the integration/merge surface.
- Governance guidance now standardizes `wt-create` as the normal path and downgrades raw `git worktree add` to manual fallback plus `freely sync-tooling`.

## Verification Snapshot

- Passed in this worktree:
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `bash docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`
  - `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
  - `bash docs/system/workspace/scripts/tests/test-signal-intent-handler-cc`
  - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
  - `bash docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
  - `bash docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`
  - `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
  - `./bin/governance-check`

## Next Action

1. Keep this owner in `in_verification` and replay it to `develop`.
2. After canonical replay, verify the same worktree-boundary contract from canonical `develop`.
3. Close the owner without reopening `I-20260401-1303-A-2`.
