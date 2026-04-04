# Child Slice Status: governance-chain-legacy-repair

## Canonical Parent

- issue_id: `I-20260403-1100-A`
- current_canonical_branch: `develop`
- current_reference_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-merge-sandbox-develop`
- historical_source_research_branch: `feature/governance-chain-legacy-repair-20260403-1100`
- historical_source_research_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1100-feature-governance-chain-legacy-repair`
- historical_develop_delivery_branch: `feature/governance-chain-legacy-repair-promote-20260403-175428`
- develop_merge_commit: `de93a83`

## Relationship Facts

1. `1200/1201/1202/1203` are active repair slices for the same governance-chain unblock batch.
2. Their relationship to `1100` is governance ownership, not git ancestry.
3. Each of these branches shares the same merge-base `0f97fc0227bba66b2552a57a7611c482b19ec150` with both `develop` and `1100`.
4. Therefore `1100` must record the parent-child mapping explicitly; it cannot rely on stacked-branch inference.
5. The original `1100` branch was not safe to merge wholesale into `develop` because it carried unrelated stale commits; the canonical writeback was replayed onto a fresh promotion branch from current `develop`.
6. The original local `1100/1200/1201/1202/1203` worktrees are already retired; current routing truth must describe them as historical research surfaces, not active execution roots.

## Current Child Slice Map

1. `1200`
- historical_branch: `feature/verification-artifact-dir-repair-20260403-1200`
- historical_worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1200-feature-verification-artifact-dir-repair`
- local_disposition: `retired`
- focus: legacy `verification_artifact_dir` backfill
- current_status: `needs_research`
- parent_issue_id: `I-20260403-1100-A`
- parent_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_path: `pending://parent-routing-decision`
- owner_relation: child slice currently routed under `I-20260403-1100-A`

2. `1201`
- historical_branch: `feature/implementation-decision-note-repair-20260403-1201`
- historical_worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1201-feature-implementation-decision-note-repair`
- local_disposition: `retired`
- focus: legacy implementation decision note backfill
- current_status: `needs_research`
- parent_issue_id: `I-20260403-1100-A`
- parent_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_path: `pending://parent-routing-decision`
- owner_relation: child slice currently routed under `I-20260403-1100-A`

3. `1202`
- historical_branch: `feature/candidate-touched-repair-20260403-1202`
- historical_worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1202-feature-candidate-touched-repair`
- local_disposition: `retired`
- focus: review issue-field normalization
- current_status: `needs_research`
- parent_issue_id: `I-20260403-1100-A`
- parent_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_path: `pending://parent-routing-decision`
- owner_relation: child slice currently routed under `I-20260403-1100-A`

4. `1203`
- historical_branch: `feature/issue-id-key-repair-20260403-1203`
- historical_worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1203-feature-issue-id-key-repair`
- local_disposition: `retired`
- focus: candidate/issue key mapping and continuity backfill
- current_status: `needs_research`
- parent_issue_id: `I-20260403-1100-A`
- parent_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_path: `pending://parent-routing-decision`
- owner_relation: child slice currently routed under `I-20260403-1100-A`

## Closure Rule

- No child slice may claim `status: promoted` until it either becomes absorbed into `I-20260403-1100-A` or materializes its own lawful issue/progress chain.
- `1100` remains the umbrella owner until the child-slice normalization and legacy drift repair batch are both verified.
- The original `1100/1200/1201/1202/1203` worktrees have already been retired locally and must be treated as historical research provenance rather than future execution roots.

## Retirement Handoff

### Local disposition

- `feature/governance-chain-legacy-repair-promote-20260403-175428`: merged to `develop` and retired locally.
- `feature/governance-chain-legacy-repair-20260403-1100`: research writeback completed; local worktree/branch retired after cleanup writeback.
- `feature/verification-artifact-dir-repair-20260403-1200`: research writeback completed; local worktree/branch retired after cleanup writeback.
- `feature/implementation-decision-note-repair-20260403-1201`: research writeback completed; local worktree/branch retired after cleanup writeback.
- `feature/candidate-touched-repair-20260403-1202`: research writeback completed; local worktree/branch retired after cleanup writeback.
- `feature/issue-id-key-repair-20260403-1203`: research writeback completed; local worktree/branch retired after cleanup writeback.

### Remote disposition

- `origin/feature/governance-chain-legacy-repair-20260403-1100`: retain with reason, because the branch is not a direct `develop` ancestor even though its canonical content was replayed through the promotion lane.
- `origin/feature/verification-artifact-dir-repair-20260403-1200`: retain with reason, because the branch is not a direct `develop` ancestor even though its canonical content was absorbed by the parent repair.
- `origin/feature/implementation-decision-note-repair-20260403-1201`: retain with reason, because the branch is not a direct `develop` ancestor even though its canonical content was absorbed by the parent repair.
- Future legacy artifact backfill must reopen from current `develop`, not from any of the retained remote research branches above.
