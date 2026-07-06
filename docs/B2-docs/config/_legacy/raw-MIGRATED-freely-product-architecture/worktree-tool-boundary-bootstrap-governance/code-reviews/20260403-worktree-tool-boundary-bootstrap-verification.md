# Verification: worktree-tool-boundary-bootstrap-governance

- issue_id: `I-20260403-2041-A`
- verifier: `codex`
- branch: `feature/tool-sandbox-worktree-bootstrap-20260403-204147`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-204147-feature-tool-sandbox-worktree-bootstrap`
- issue_path: `docs/B2-docs/config/packaging/raw-20260402-0403issues/worktree-tool-boundary-bootstrap-governance.md`
- decision_note: `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260403-worktree-tool-boundary-bootstrap-implementation-decision.md`

## Scope

Verify the narrow follow-on that extends Freely's managed tool boundary contract from the project root into sibling worktrees without weakening the protected-root distinction.

## Checks

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

## Result

- pass: managed tool boundary bootstrap now rematerializes in sibling worktrees through explicit sync, `wt-create`, and protected-branch auto-worktree paths
- pass: `iflow` launcher now receives the sibling worktrees root as an explicit boundary extension
- pass: docs and hook guidance now point at `wt-create` as the standard path and treat raw `git worktree add` as fallback plus `freely sync-tooling`
- pass: lifecycle writeback and implementation decision note satisfy the current governance gate

## Residual Risk

- Tools without a verified project-local config surface still depend on wrapper and launch-time boundary extension; that remains intentional for now.
