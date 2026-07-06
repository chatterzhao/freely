# Progress: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

- issue_id: `I-20260405-2358-A`
- issue_path: `docs/B2-docs/config/packaging/raw-20260402-0403issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- title: `Fresh-project bootstrap and baseline scoping followthrough governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/fresh-project-bootstrap-baseline-scoping-closeout-20260406-2025`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2025-feature-fresh-project-bootstrap-baseline-scoping-closeout`
- updated_at: `2026-04-06`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical `develop` now carries the narrow fresh-project bootstrap repair: `sync-tooling` retargets copied config truth to the requested project and rematerializes `.githooks`.
- Focused regression coverage proves the repair survives both premerge integration and post-merge followthrough while keeping `baseline-status` and `status --view baseline` pinned to the target project.
- Adjacent runtime/control-plane and CLI help/dry-run owners remain explicitly out of scope; this owner closes as a bounded bootstrap/scoping slice.

## Completion Evidence

- `develop` merge `65553c9`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-status-family`
- `./bin/governance-check`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1935-test-pre-merge-fresh-project-bootstrap-baseline-scoping-followthrough --issue docs/B2-docs/config/packaging/raw-20260402-0403issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/B2-docs/config/packaging/raw-20260402-0403issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- `git diff --check`
- `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` regresses fresh-project bootstrap scoping, hook rematerialization, or baseline/status target pinning.
