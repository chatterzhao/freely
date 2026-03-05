---
name: premerge-reconcile
description: Reconcile high-risk merge conflicts without governance rollback. Use when merge-train into pre-develop fails or semantic regression risk appears; create temporary premerge branch from pre-develop, resolve by semantic intent, merge back to pre-develop, and clean up.
---

# skill:premerge-reconcile

## Trigger
- Normal merge into `pre-develop` fails with high-conflict files.
- Risk of policy rollback after conflict resolution.

## Preconditions
- Start from current `pre-develop`.
- Create dedicated branch:
  - `git branch feature/premerge-YYYYMMDD-HHMM--<topic> pre-develop`
  - enter via worktree (`source ./bin/wt-enter ...`).

## Workflow
1. Reconcile via controlled integration:
   - merge or cherry-pick needed commits into `feature/premerge-*`
   - resolve conflicts with semantic-first decisions
2. For each conflict, follow `references/conflict-decision-template.md`.
3. Run minimal regression on this branch.
4. Merge back only to `pre-develop`:
   - `git checkout pre-develop`
   - `git merge --no-ff feature/premerge-...`
5. Run semantic regression checks via `skill:branch-management` checklist.
6. Cleanup:
   - delete premerge branch and worktree
   - record outcome in progress/recovery notes.

## Conflict Rule
- Prefer semantic compatibility with current constitution/laws.
- If old structure conflicts with current governance, keep governance and adapt old content.

## Done
- `pre-develop` contains reconciled changes.
- Regression checks pass.
- Premerge branch/worktree removed.
