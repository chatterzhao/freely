---
name: dev-loop-execution
description: Execute D:dev-loop(DDD) workflows with document-read, implementation, testing, and document-update closure. Use when AI performs code changes under governed issue/story context.
---

# skill:dev-loop-execution

## Workflow
1. Read governing docs and issue context.
2. Implement changes in correct feature worktree.
3. If code and docs are inconsistent, prioritize code/test correction path first.
4. During development and review, continuously add/adjust test cases based on implementation and defects found.
5. Run required tests, including integration acceptance tests, and treat `TEST` results as merge/promotion evidence.
6. Update progress/issue status documents with test evidence.
7. Validate closure with `skill:laws-enforcer` and `skill:constitution-guard`.

## Done
- Code, tests, and doc status updates are aligned and verifiable.
