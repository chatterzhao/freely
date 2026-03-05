# skill:premerge-reconcile

## Purpose
Handle complex merge conflicts without governance regression by using a temporary `premerge` feature branch.

## Trigger
- Normal merge into `pre-develop` fails with high-conflict files.
- Risk of policy rollback after conflict resolution.

## Preconditions
- Start from current `pre-develop`.
- Create dedicated branch:
  - `git branch feature/premerge-YYYYMMDD-HHMM--<topic> pre-develop`
  - enter via worktree (`source ./bin/wt-enter ...`).

## Steps
1. Reconcile via controlled integration:
   - merge or cherry-pick needed commits into `feature/premerge-*`
   - resolve conflicts with semantic-first decisions
2. For each resolved conflict, record:
   - file
   - competing intents
   - chosen intent and rationale
3. Run minimal regression on this branch.
4. Merge back only to `pre-develop`:
   - `git checkout pre-develop`
   - `git merge --no-ff feature/premerge-...`
5. Run `skill:post-merge-regression`.
6. Cleanup:
   - delete premerge branch and worktree
   - record outcome in progress/recovery notes.

## Conflict Rule
- Prefer semantic compatibility with current constitution/laws.
- If old structure conflicts with current governance, keep governance and adapt old content.

## Done When
- `pre-develop` contains reconciled changes.
- Regression checks pass.
- Premerge branch/worktree removed.
