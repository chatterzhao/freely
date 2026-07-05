# Candidates

## C-20260620T113909Z-A: legacy issue
- status: promoted
- milestone: M-20260620T113909Z-A
- promoted_issue_path: docs/issues/I-20260620T113909Z-A/issue.md
- summary: Add auto-push to all platforms in pr-review-guarded after committing review document
- rationale: pr-create-guarded already auto-pushes; pr-review-guarded inconsistency breaks pr-merge-guarded
- acceptance: pr-review-guarded pushes review commit to all platforms automatically, no manual git push needed
- next: Materialize as I-20260620T113909Z-A, merge via PR
