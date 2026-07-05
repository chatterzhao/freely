# Brainstorm: milestone-completed-queue-closeout-governance

1. The failure is not a new milestone policy question. The policy already says `phase_state=completed` belongs in `completed_issues`.
2. Manual cleanup alone is too weak because the baseline repo audit currently allows historical queue drift to sit silently on canonical `develop`.
3. The narrow fix is:
   - repair `docs/milestones.md`
   - teach `governance-check` to compare queue placement with issue `phase_state`
   - lock it with one focused regression
