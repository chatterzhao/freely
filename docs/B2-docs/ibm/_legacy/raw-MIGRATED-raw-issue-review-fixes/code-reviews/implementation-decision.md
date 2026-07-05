# Implementation Decision: raw issue completeness fixes
- issue_id: I-20260618T024841Z-A
- decision: Three small fixes — sync candidate acceptance_criteria to actual implementation, add wt-close guard to copy raw issue to develop before worktree deletion
- why_this: Candidate drift undermines governance traceability. Missing raw issue after wt-close causes data loss and broken lifecycle links.
- alternatives_considered: Auto-sync candidate from implementation — rejected, too complex for now. Keep raw issues only in develop — rejected, defeats the purpose of worktree autonomy.
- boundary_non_goals: Not adding automated candidate-implementation consistency checking. Not changing raw-issue-pull behavior.
- residual_risk: None.
