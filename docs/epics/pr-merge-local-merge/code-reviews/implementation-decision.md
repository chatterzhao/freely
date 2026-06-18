# Implementation Decision: local merge replaces gh pr merge
- issue_id: I-20260618T065221Z-A
- decision: Replace gh pr merge --merge with local git merge --no-ff. Add platform consistency check to wt-create.
- why_this: gh pr merge --merge --body does not work (GitHub API limitation). Receipt never enters merge commit, causing hook blocks and platform divergence.
- alternatives_considered: gh pr merge --squash — rejected, changes commit history. Fix --body to work — impossible, GitHub API ignores --body for --merge.
- boundary_non_goals: Not changing _sync_prs_across_platforms. Not removing gh CLI dependency entirely.
- residual_risk: gh pr close may fail silently. Fallback: GitHub auto-detects merged branch and closes PR.
