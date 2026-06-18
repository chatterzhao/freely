# Implementation Decision: local merge replaces gh pr merge
- issue_id: I-20260618T071502Z-A
- decision: Replace gh pr merge --merge with local git merge --no-ff + Freely-Merge-Path receipt
- why_this: gh pr merge --merge --body is non-functional (GitHub API ignores --body for --merge). Receipt never enters GitHub merge commit.
- alternatives_considered: gh pr merge --squash — rejected, changes commit history. Fix gh pr merge to accept --body — impossible, GitHub API limitation.
- boundary_non_goals: Not removing gh CLI dependency entirely. Not changing _sync_prs_across_platforms.
- residual_risk: gh pr close may fail silently. Fallback: GitHub auto-detects merged branch and closes PR.
