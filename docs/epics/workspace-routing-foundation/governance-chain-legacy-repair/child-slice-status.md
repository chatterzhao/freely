# Child Slice Status: governance-chain-legacy-repair

## Canonical Parent

- issue_id: `I-20260403-1100-A`
- branch: `feature/governance-chain-legacy-repair-20260403-1100`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1100-feature-governance-chain-legacy-repair`

## Relationship Facts

1. `1200/1201/1202/1203` are active repair slices for the same governance-chain unblock batch.
2. Their relationship to `1100` is governance ownership, not git ancestry.
3. Each of these branches shares the same merge-base `0f97fc0227bba66b2552a57a7611c482b19ec150` with both `develop` and `1100`.
4. Therefore `1100` must record the parent-child mapping explicitly; it cannot rely on stacked-branch inference.

## Current Child Slice Map

1. `1200`
- branch: `feature/verification-artifact-dir-repair-20260403-1200`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1200-feature-verification-artifact-dir-repair`
- focus: legacy `verification_artifact_dir` backfill
- current_status: `needs_research`
- promoted_issue_path: `pending://owned-by-c-20260403-1100-a`
- owner_relation: child slice of `C-20260403-1100-A`

2. `1201`
- branch: `feature/implementation-decision-note-repair-20260403-1201`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1201-feature-implementation-decision-note-repair`
- focus: legacy implementation decision note backfill
- current_status: `needs_research`
- promoted_issue_path: `pending://owned-by-c-20260403-1100-a`
- owner_relation: child slice of `C-20260403-1100-A`

3. `1202`
- branch: `feature/candidate-touched-repair-20260403-1202`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1202-feature-candidate-touched-repair`
- focus: review issue-field normalization
- current_status: `needs_research`
- promoted_issue_path: `pending://issue-materialization`
- owner_relation: child slice of `C-20260403-1100-A`

4. `1203`
- branch: `feature/issue-id-key-repair-20260403-1203`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-1203-feature-issue-id-key-repair`
- focus: candidate/issue key mapping and continuity backfill
- current_status: `needs_research`
- promoted_issue_path: `pending://issue-materialization`
- owner_relation: child slice of `C-20260403-1100-A`

## Closure Rule

- No child slice may claim `status: promoted` until it either becomes absorbed into `I-20260403-1100-A` or materializes its own lawful issue/progress chain.
- `1100` remains the umbrella owner until the child-slice normalization and legacy drift repair batch are both verified.
