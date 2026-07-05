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
- A guarded `test-pre-merge` replay also proved the remaining gap was not a broken hook but missing owner truth: develop-bound promote demanded an explicit `premerge-integration:develop_merge` adequacy item, which is now recorded in the owner pre-tests.
- This owner is also the absorbing lifecycle for `C-20260411-1414-B`, the follow-on adequacy candidate intentionally split out of the launch-time hard-gate brainstorm to keep runtime enforcement and schema expansion on separate tracks.
- This lane is already closed on canonical `develop`: focused feature-lane and premerge-lane regressions, guarded promotion, and dedicated-lane retirement are complete, so this progress file is now historical closeout evidence rather than an active execution pointer.

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `./bin/governance-check`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`
- `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`

## Next Action

`completed`
