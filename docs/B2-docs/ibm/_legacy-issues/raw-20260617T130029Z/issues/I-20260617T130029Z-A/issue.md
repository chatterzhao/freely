- issue_id: I-20260617T130029Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260617T130029Z-A
- source_candidate: docs/B1-docs/raw-20260617T130029Z29Z-pr-create-conflict-abort/candidates.md#C-20260617T130029Z-A
- verification_artifact_dir: docs/B2-docs/pr-create-conflict-abort/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260617T130029Z-A/issue.md
- title: pr-create-guarded conflict handling — show conflicted files + abort

# I-20260617T130029Z-A: pr-create-guarded conflict handling

- title: Show conflicted files and abort path when pr-create-guarded hits merge conflicts
- source: `raw-20260617T130029Z29Z` (GitHub #2925)
- milestone: M-20260617T130029Z-A
- source_candidate: `docs/B1-docs/raw-20260617T130029Z29Z-pr-create-conflict-abort/candidates.md#C-20260617T130029Z-A`
- issue_id: I-20260617T130029Z-A
- phase_state: completed
- component: worktree

## Implementation
- Modified `docs/system/workspace/scripts/worktree/pr-create-guarded` conflict handler
- Added `git diff --name-only --diff-filter=U` conflicted file listing
- Added `git merge --abort` abort path as alternative to manual resolution
