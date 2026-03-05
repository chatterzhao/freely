# System Workspace Skills

This directory is the execution source for Freely autonomous workflow.

Rules:
- `CONSTITUTION.md` and `LAWS.md` define constraints and acceptance.
- Skills define executable steps for AI agents.
- When conflicts occur, prefer semantic intent over commit time order.
- Do not duplicate full execution procedures in multiple docs.

Entry skills:
- `skill:branch-management` -> `branch-management/SKILL.md`
- `skill:premerge-reconcile` -> `premerge-reconcile/SKILL.md`

Design:
- Keep one main branch-governance skill (`branch-management`) for normal flow.
- Keep one exception skill (`premerge-reconcile`) for high-conflict recovery.
