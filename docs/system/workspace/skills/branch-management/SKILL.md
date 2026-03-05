---
name: branch-management
description: Manage full autonomous branch lifecycle for Freely-style development. Use when AI needs to create feature branches from pre-develop, enter worktrees, perform add/commit in correct place, run merge-train into pre-develop with immediate tests, execute semantic regression checks, promote to develop, manage release/hotfix branches, apply stage-based tags, and clean up branches/worktrees after verification.
---

# skill:branch-management

## Route A: Feature Development
1. Create feature branch from `pre-develop`:
   - `git branch feature/<topic> pre-develop`
2. Enter branch worktree (auto-create + cd):
   - `source ./bin/wt-enter feature/<topic>`
3. Do changes in this worktree only.
4. Stage and commit in feature worktree:
   - `source ./bin/wt-add feature/<topic> -- <paths or -A>`
   - `git commit -m "<type>: <summary>"`
5. Run branch-local tests before integration.

## Route B: Merge Train to pre-develop
1. Work only from the `pre-develop` worktree for integration.
2. Collect candidates with `git branch --no-merged pre-develop`.
3. Build merge queue by semantic dependency, never by commit time:
   - governance/policy changes
   - shared infra
   - product behavior changes
4. Merge serially:
   - `git merge --no-ff <branch>`
   - run required smoke/regression checks immediately
5. If conflict is complex or rollback risk appears, stop and switch to `skill:premerge-reconcile`.

## Route C: Regression + Promotion
1. After queue completion, run semantic checklist:
   - `references/semantic-regression-checklist.md`
2. If green, promote `pre-develop` to `develop` through allowed path.
3. If any semantic mismatch appears, block promotion and return to reconcile flow.

## Route D: Release and Tag Flow
1. Follow stage naming from `references/release-tag-policy.md`:
   - format: `YYYY.MM.DD-HHMM-stage`
2. Tag behavior by branch/stage:
   - `feature/*` -> `alpha` (local lightweight tag, no push)
   - `pre-develop` -> `beta` (local lightweight tag, no push)
   - `develop` -> `nightly` (push tag)
   - `main` -> `stable` (push tag)
   - `hotfix/*` -> `hotfix` (push tag)
3. Release branch path:
   - create `release/*` from `develop`
   - merge to `main`
   - back-merge to `develop`
4. Hotfix branch path:
   - create `hotfix/*` from `main`
   - merge to `main` and `develop`
   - sync hotfix result to `pre-develop`
5. If any required verification is red, block push tag/release.

## Route E: Cleanup Policy
1. Do not delete branch/worktree immediately after merge.
2. Keep status progression:
   - `active` -> `merged-pending-verify` -> `verified-retirable` -> `retired`
3. Delete branch/worktree only after:
   - merge complete
   - tests and semantic regression green
   - no pending rollback item

## Hard Rules
- Never deliver feature branches directly to `develop`.
- Keep governance intent stable: branch policy, worktree constraints, naming policy.
- If semantic checks fail, do not promote; return to reconcile flow.
- Never resolve conflicts by commit timestamp ordering.
- Never push `alpha`/`beta` tags.

## Done
- No branch remains in `git branch --no-merged pre-develop`.
- Semantic regression checklist is fully green.
- Promotion/tag/release actions are completed or explicitly blocked with recorded reason.
