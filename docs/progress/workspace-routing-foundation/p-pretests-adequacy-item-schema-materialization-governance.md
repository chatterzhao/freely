# Progress: pretests-adequacy-item-schema-materialization-governance

- issue_id: `I-20260411-1415-A`
- title: Pre-tests adequacy item schema materialization governance
- phase_state: `completed`
- runtime_state: `stopped`
- branch: `feature/pretests-adequacy-item-schema-materialization-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-pretests-adequacy-item-schema-materialization`
- issue_path: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/issues/pretests-adequacy-item-schema-materialization-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-closeout"}

## Summary

- This lane turned the previously implicit adequacy judgment into machine-readable Acceptance Item metadata instead of relying on generic pass artifacts.
- `pretests-gate` now separates three failure classes for guarded promote: no adequacy-v2 item for the requested lane/gate pair, adequate item present but not backed by sufficient evidence, and stale/non-staged artifact reuse.
- `governance-merge-gate` now requires owner `verification_artifact_dir` to stay scoped to `docs/epics/.../code-reviews`, so broad directories cannot smuggle unrelated staged files into develop-bound promote evidence.
- The hook path itself is covered: the updated `test-pre-merge-commit-hook` fixture now uses adequacy-v2 fields and proves docs-only `test-pre-merge` closeout still blocks until fresh owner-scoped evidence is staged.
- This worktree has completed focused regressions and governance verification; the next step is guarded promotion into canonical `develop`, then retirement of this dedicated lane and its temporary promote batch.

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `./bin/governance-check`
- `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`

## Next Action

`completed`
