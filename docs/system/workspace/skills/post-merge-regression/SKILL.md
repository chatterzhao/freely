# skill:post-merge-regression

## Purpose
Immediately verify merged state and detect rollback of governance intent.

## Trigger
- After every merge into `pre-develop`.
- After premerge reconciliation merge-back.

## Preconditions
- On `pre-develop`.
- Working tree clean after merge commit.

## Checks
1. Branch governance intent:
   - `feature/*` from `pre-develop`
   - `main/develop/pre-develop` add/commit blocked
2. Worktree governance intent:
   - root must be sibling `{project-name}-worktrees`
   - creation inside project root forbidden
3. Pre-brainstorms naming intent:
   - `YYYYMMDD-HHMM--<topic>`
4. Premerge policy intent:
   - `feature/premerge-YYYYMMDD-HHMM--<topic>`
   - must start from and merge back to `pre-develop`

## Method
- Validate by semantic assertions in docs + hooks/scripts.
- Do not treat commit timestamp as correctness signal.
- If intent mismatch found, stop promotion and route to `skill:premerge-reconcile`.

## Done When
- All assertions pass.
- No known rollback signal remains.
