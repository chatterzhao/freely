# Implementation Decision
- issue_id: I-20260618T043121Z-A
- decision: git status --porcelain for pr-create (catches untracked) + develop check for pr-merge
- why_this: git diff --quiet only checks tracked files. Untracked raw issues would be missed.
- alternatives_considered: git clean -n — rejected, doesn't show staged changes
- boundary_non_goals: Not adding .gitignore management
- residual_risk: None
