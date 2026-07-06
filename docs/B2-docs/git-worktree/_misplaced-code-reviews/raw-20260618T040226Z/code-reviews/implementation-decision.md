# Implementation Decision: pr-review-guarded
- issue_id: I-20260618T040226Z-A
- decision: New pr-review-guarded command between pr-create and pr-merge. 6 review dimensions → verdict document → pr-merge-guarded gates on verdict=pass. Update all 18+ workflow references.
- why_this: ef251886/15fa666c showed git auto-merge silently drops functionality. Industry standard requires independent review before merge. Freely needs machine-readable review verdict that persists in the repo.
- alternatives_considered: Add checks to existing pr-merge-guarded — rejected, conflates review and merge concerns. Use only GitHub PR review — rejected, GitHub review comments aren't version-controlled in the repo.
- boundary_non_goals: Phase 2 GitHub PR review API sync. Extensible review dimensions (future enhancement). Automated AI reviewer subagent (future enhancement).
- residual_risk: Review is only as good as its dimensions. New invariant types may need new checks added manually.
