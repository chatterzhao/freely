---
name: branch-management
description: Manage autonomous branch flow for Freely-style development. Use when AI needs to integrate multiple feature branches into pre-develop, run merge-train with immediate tests, perform semantic regression checks, and promote pre-develop to develop after gates pass.
---

# skill:branch-management

## Workflow
1. Work only from the `pre-develop` worktree for integration.
2. Collect candidates with `git branch --no-merged pre-develop`.
3. Build merge queue by semantic dependency, never by commit time:
   - governance/policy changes
   - shared infra
   - product behavior changes
4. Merge serially (`git merge --no-ff <branch>`), test immediately after each merge.
5. If conflict is complex or rollback risk appears, stop and switch to `skill:premerge-reconcile`.
6. After queue completion, run semantic regression checklist in `references/semantic-regression-checklist.md`.
7. If all gates pass, promote `pre-develop` to `develop` through allowed merge path.

## Hard Rules
- Never deliver feature branches directly to `develop`.
- Keep governance intent stable: branch policy, worktree constraints, naming policy.
- If semantic checks fail, do not promote; return to reconcile flow.

## Done
- No branch remains in `git branch --no-merged pre-develop`.
- Semantic regression checklist is fully green.
- Promotion to `develop` is completed or explicitly blocked with recorded reason.
