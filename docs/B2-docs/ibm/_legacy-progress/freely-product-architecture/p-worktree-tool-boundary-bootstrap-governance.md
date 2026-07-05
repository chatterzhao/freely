# Progress: worktree-tool-boundary-bootstrap-governance

- issue_id: `I-20260403-2041-A`
- issue_path: `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
- title: `Worktree tool boundary bootstrap governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/worktree-tool-boundary-bootstrap-closeout-20260405-1700`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-1700-feature-worktree-tool-boundary-bootstrap-closeout`
- updated_at: `2026-04-05`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner is the narrow follow-on for the sibling-worktree gap left after the completed tool-materialization slice.
- `freely sync-tooling` is now the canonical rematerialization primitive for project-local tool boundaries.
- `wt-create` and protected-branch `post-checkout` auto-worktree creation now call that primitive, so ignored or untracked local tool directories do not strand the boundary contract in the project root.
- `tool-launchers.sh` now extends supported tool boundaries to the sibling worktrees root at launch time, while keeping the project root as the integration/merge surface.
- Governance guidance now standardizes `wt-create` as the normal path and downgrades raw `git worktree add` to manual fallback plus `freely sync-tooling`.

## Completion Evidence

- `develop` merge `eaddfc8`
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
- `git diff --check`
- `./bin/governance-check`
- `docs/B2-docs/config/packaging/code-reviews/20260403-worktree-tool-boundary-bootstrap-verification.md`
- `docs/B2-docs/config/packaging/code-reviews/20260405-worktree-tool-boundary-bootstrap-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` regresses sibling-worktree tooling rematerialization or the tool-boundary split drifts again.
