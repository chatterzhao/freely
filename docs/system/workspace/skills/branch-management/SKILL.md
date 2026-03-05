---
name: branch-management
description: Manage full autonomous branch lifecycle for Freely-style development. Use when AI needs to create feature branches from pre-develop, enter worktrees, perform add/commit in correct place, run merge-train into pre-develop with immediate tests, execute semantic regression checks, promote to develop, manage release/hotfix branches, apply stage-based tags, and clean up branches/worktrees after verification.
---

# skill:branch-management

## Route A: Feature Development
1. Run preflight guards:
   - `skill:constitution-guard`
   - `skill:laws-enforcer`
2. Create feature branch from `pre-develop`:
   - `git branch feature/<topic> pre-develop`
3. Enter branch worktree (auto-create + cd):
   - `source ./bin/wt-enter feature/<topic>`
4. Do changes in this worktree only.
5. Stage and commit in feature worktree:
   - `source ./bin/wt-add feature/<topic> -- <paths or -A>`
   - `git commit -m "<type>: <summary>"`
6. Run branch-local tests before integration.

## Route B: Merge Train to pre-develop
1. Work only from the `pre-develop` worktree for integration.
2. Run `./bin/wt-status-all`; if any worktree is `DIRTY`, block merge train.
3. Audit candidates with `./bin/branch-merge-audit --only-unmerged` (must include source branch and target merge status).
4. Build merge queue by semantic dependency, never by commit time:
   - governance/policy changes
   - shared infra
   - product behavior changes
5. Merge serially:
   - `git merge --no-ff <branch>`
   - run required smoke/regression checks immediately
6. If conflict is complex or rollback risk appears, stop and switch to `skill:premerge-reconcile`.

## Route C: Regression + Promotion
1. After queue completion, run semantic checklist:
   - `references/semantic-regression-checklist.md`
2. Run `./bin/wt-status-all`; promotion is blocked unless all worktrees are `CLEAN`.
3. Run required `TEST` evidence check for promotion (including integration acceptance tests).
4. Ensure `PRE_TEST` remains baseline-only and is not used as substitute for promotion test results.
5. If all checks are green, promote `pre-develop` to `develop` through allowed path.
6. If any semantic/test mismatch appears, block promotion and return to reconcile flow.

## Route D: Release and Tag Flow
1. Follow stage naming from `references/release-tag-policy.md`:
   - format: `YYYY.MM.DD-HHMM-stage`
2. Run `./bin/wt-status-all`; release/tag actions are blocked unless all worktrees are `CLEAN`.
3. Tag behavior by branch/stage:
   - `feature/*` -> `alpha` (local lightweight tag, no push)
   - `pre-develop` -> `beta` (local lightweight tag, no push)
   - `develop` -> `nightly` (push tag)
   - `main` -> `stable` (push tag)
   - `hotfix/*` -> `hotfix` (push tag)
4. Release branch path:
   - create `release/*` from `develop`
   - merge to `main`
   - back-merge to `develop`
5. Hotfix branch path:
   - create `hotfix/*` from `main`
   - merge to `main` and `develop`
   - sync hotfix result to `pre-develop`
6. If any required verification is red, block push tag/release.

## Route E: Cleanup Policy
1. Do not delete branch/worktree immediately after merge.
2. Keep status progression:
   - `active` -> `merged-pending-verify` -> `verified-retirable` -> `retired`
3. Run `./bin/wt-status-all` before cleanup; if any worktree is `DIRTY`, block cleanup and resolve first.
4. Delete branch/worktree only after:
   - merge complete
   - tests and semantic regression green
   - no pending rollback item

## Hard Rules
- Never deliver feature branches directly to `develop`.
- Keep governance intent stable: branch policy, worktree constraints, naming policy.
- If semantic checks fail, do not promote; return to reconcile flow.
- Never resolve conflicts by commit timestamp ordering.
- Never push `alpha`/`beta` tags.
- For normative doc changes, keep work in dedicated feature/worktree and require linked implementation or gate-change evidence.
- Merge/promotion/release/cleanup require `./bin/wt-status-all` all `CLEAN`.

## Done
- No branch remains in `git branch --no-merged pre-develop`.
- Semantic regression checklist is fully green.
- Promotion/tag/release actions are completed or explicitly blocked with recorded reason.
