---
name: dev-loop-execution
description: Execute D:dev-loop(DDD) workflows with document-read, implementation, testing, and document-update closure. Use when AI performs code changes under governed issue/story context.
---

# skill:dev-loop-execution

## Workflow
1. Read governing docs and issue context.
2. Before implementation, define current cycle's semantic scope and avoid mixing unrelated concerns in one commit.
3. Implement changes in correct feature worktree.
4. If code and docs are inconsistent, prioritize code/test correction path first.
5. During development and review, continuously add/adjust test cases based on implementation and defects found.
6. Before push/merge, perform semantic commit-boundary re-check; split commits if mixed concerns remain.
7. Run required tests, including integration acceptance tests, and treat `TEST` results as merge/promotion evidence.
8. Update progress/issue status documents with test evidence.
9. Validate closure with `skill:laws-enforcer` and `skill:constitution-guard`.

## Done
- Code, tests, and doc status updates are aligned and verifiable.
