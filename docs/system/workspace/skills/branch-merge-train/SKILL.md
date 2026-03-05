# skill:branch-merge-train

## Purpose
Serially merge multiple `feature/*` branches into `pre-develop` with immediate tests after each merge.

## Trigger
- Multiple active worktrees/feature branches need integration.
- Agent receives instruction like: "merge all into pre-develop".

## Preconditions
- Work in the `pre-develop` worktree.
- Working tree is clean before starting.
- Merge queue is explicit and ordered by semantic dependency (not commit time).

## Steps
1. Collect candidates: `git branch --no-merged pre-develop`.
2. Build merge queue by semantic order:
   - governance and branch policy first
   - shared infra changes next
   - feature behavior changes last
3. For each branch in queue:
   - `git merge --no-ff <branch>`
   - run required smoke/regression checks immediately
   - if tests fail, stop queue and enter `skill:premerge-reconcile`
4. After queue finished:
   - run full post-merge checks via `skill:post-merge-regression`
   - record merge summary and any risk notes.

## Conflict Rule
- Resolve conflicts by semantic intent.
- Never choose content by "latest commit time".
- Preserve current governance model if conflict is between old and new rules.

## Done When
- No target branch remains in `git branch --no-merged pre-develop`.
- Post-merge regression checks pass.
