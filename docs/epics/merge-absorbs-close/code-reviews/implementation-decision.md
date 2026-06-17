# Implementation Decision: pr-merge-guarded absorbs wt-close
- issue_id: I-20260617T124129Z-A
- decision: pr-merge-guarded writes close frontmatter into merge commit, wt-close removes worktree only
- why_this: Eliminates dirty develop from wt-close FREELY_SKIP_IBM_GATE commits
- alternatives_considered: wt-close push after commit — rejected: still violates develop commit policy
- boundary_non_goals: wt-close still closes platform issues (GitHub API)
- residual_risk: Must verify raw_key extraction from branch name works for all formats
