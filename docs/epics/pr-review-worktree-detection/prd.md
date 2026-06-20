# PRD: pr-review-guarded fixes

## Problems
1. No branch arg → defaulted to current branch, unclear
2. Gate ran from develop root → IBM completeness false negatives
3. Review doc missing issue_id → pr-merge gate failure

## Fixes
1. Branch arg required
2. cd into worktree before gate
3. Auto-generate issue_id in review doc
