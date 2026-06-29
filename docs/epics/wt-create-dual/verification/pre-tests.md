# Pre-Tests: wt-create Dual Worktree Creation

- issue_id: raw-20260506T1230Z

## Unit
- acceptance target: `CLI parsing accepts valid args, rejects invalid args.`
- testing layer: `unit`
- target environment: `feature/raw-20260506T1230Z-wt-create-dual`
- required evidence: `bash -n syntax check + CLI arg parsing tests`
- blocker taxonomy: `execution_pending_or_failed`
1. Test --help output
2. Test missing args rejection
3. Test invalid prefix rejection
4. Test invalid raw-key rejection

## Integration
- acceptance target: `wt-create creates two worktrees with correct parent relationship.`
- testing layer: `integration`
- target environment: `feature/raw-20260506T1230Z-wt-create-dual`
- required evidence: `git merge-base check confirms fix is descendant of test-pre-merge`
- blocker taxonomy: `execution_pending_or_failed`
1. Run wt-create --raw-key --prefix --skill --slug
2. Verify two worktrees created
3. Verify merge-base(fix, tp) == tp HEAD
4. Verify legacy interface still works

## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes all gates.`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge feature branch into test-pre-merge via freely pr-merge-guarded.
2. Merge test-pre-merge into develop via freely pr-merge-guarded.
3. Verify Freely-Merge-Path trailers in merge commit messages.

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Pure script change. Verified via unit and integration tests.`

## Acceptance Items

### AT-001 dual worktree creation
- id: `dual-create`
- requirement: `wt-create --raw-key --prefix --skill --slug creates test-pre-merge + fix/feature worktrees.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: ``
- case_design: `Run wt-create with valid args, verify two worktrees, check parent relationship.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/wt-create-dual/code-reviews/review.md`

### AT-002 fast-forward merge
- id: `fast-forward`
- requirement: `fix→test-pre-merge is fast-forward (merge-base == tp HEAD).`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: ``
- case_design: `Create commit on fix branch, verify merge-base(fix, tp) == tp HEAD.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/wt-create-dual/code-reviews/review.md`
