# Candidates: pr-review-guarded worktree detection + auto issue_id

## C-20260620T142847Z-A
- title: pr-review-guarded requires branch, uses worktree context, auto-generates issue_id
- status: promoted
- promoted_issue_path: docs/issues/I-20260620T142847Z-A/issue.md
- milestone: M-20260620T142847Z-A
- summary: |
    Three fixes to pr-review-guarded:
    1. Branch arg required (no default to current branch)
    2. cd into fix worktree before IBM gate so it reads correct docs
    3. Auto-generate issue_id from raw-key in review doc
