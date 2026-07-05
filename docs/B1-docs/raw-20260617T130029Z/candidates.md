# Candidates: pr-create-guarded conflict handling improvements

## C-20260617T130029Z-A
- title: Show conflicted files and abort path when pr-create-guarded hits merge conflicts
- status: promoted
- promoted_issue_path: docs/issues/I-20260617T130029Z-A/issue.md
- milestone: M-20260617T130029Z-A
- summary: |
    When git pull triggers merge conflicts during pr-create-guarded,
    the error message is generic — no conflicted files listed, no
    abort path provided. This adds `git diff --name-only --diff-filter=U`
    output and a `git merge --abort` option.
