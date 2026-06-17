# Fix pull || true
- issue_id: I-20260617T131746Z-A
- decision: Replace pull || true with fetch+reset fallback
- why_this: pull || true swallows failure → push no-ops → manual push required
- alternatives_considered: Keep || true — rejected
- boundary_non_goals: Only post-merge sync in pr-merge-guarded
- residual_risk: reset --hard discards local-only develop commits (shouldn't exist after frontmatter fix)
