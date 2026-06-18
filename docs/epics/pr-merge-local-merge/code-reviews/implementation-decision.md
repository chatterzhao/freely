# Implementation Decision
- issue_id: I-20260618T065221Z-A
- decision: Replace gh pr merge --merge with local git merge --no-ff. Add platform consistency check to wt-create.
- why_this: gh pr merge --merge --body is non-functional. Receipt never enters GitHub merge commit. Hook blocks pull. Platforms diverge.
- alternatives_considered: gh pr merge --squash — rejected, changes history. Fix --body to work — impossible, GitHub API limitation.
- boundary_non_goals: Not changing _sync_prs_across_platforms (still closes remaining open PRs)
- residual_risk: gh pr close may fail silently. Fallback: GitHub auto-detects merged branch and closes PR.
