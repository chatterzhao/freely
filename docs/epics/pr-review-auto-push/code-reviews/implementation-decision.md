# Implementation Decision
- issue_id: I-20260618T060624Z-A
- decision: Auto-push to all non-all remotes after committing review document
- why_this: PR tracks branch. Without push, review doc stays local, pr-merge can't find it.
- alternatives_considered: Run pr-review before pr-create — rejected, review needs PR number
- boundary_non_goals: Not changing pr-create flow
- residual_risk: None. Push is idempotent.
