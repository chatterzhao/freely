# Semantic Regression Checklist

Run after merges into `pre-develop` and before promotion:

1. Branch governance intent:
- `feature/*` must originate from `pre-develop`.
- `main/develop/pre-develop` must remain add/commit-blocked.

2. Worktree governance intent:
- Worktree root must be sibling `{project-name}-worktrees`.
- Creating worktree inside project root must remain forbidden.

3. Pre-brainstorms naming intent:
- New record IDs use `YYYYMMDD-HHMM--<topic>`.

4. Premerge policy intent:
- Temporary reconcile branch name uses `feature/premerge-YYYYMMDD-HHMM--<topic>`.
- Reconcile flow starts from and merges back to `pre-develop`.

5. Decision method:
- Evaluate by semantic compatibility, not commit time order.
