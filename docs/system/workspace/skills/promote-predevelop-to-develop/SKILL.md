# skill:promote-predevelop-to-develop

## Purpose
Promote validated integration from `pre-develop` to `develop` safely.

## Trigger
- Merge train and post-merge regression are both green.

## Preconditions
- `pre-develop` includes all intended feature branches.
- `skill:post-merge-regression` passed.
- Required review/test evidence exists.

## Steps
1. Confirm promotion gate:
   - required tests passed
   - no unresolved conflict notes
2. Promote with traceability:
   - merge `pre-develop` into `develop` through allowed path
3. Run post-promotion checks on `develop`.
4. If any regression appears:
   - block further promotion/release
   - open reconcile branch from `pre-develop`.

## Rule
- Never bypass `pre-develop` for feature delivery.
- Promotion is blocked if governance intent is not preserved.

## Done When
- `develop` reflects validated `pre-develop` state.
- Post-promotion checks pass.
