# System Workspace Skills

This directory is the execution source for Freely autonomous workflow.

Rules:
- `CONSTITUTION.md` and `LAWS.md` define constraints and acceptance.
- Skills define executable steps for AI agents.
- When conflicts occur, prefer semantic intent over commit time order.
- Do not duplicate full execution procedures in multiple docs.
- Worktree hygiene gate command: `./bin/wt-status-all` (all `CLEAN` required before merge/promotion/release/cleanup).

Entry skills:
- `skill:constitution-guard` -> `constitution-guard/SKILL.md`
- `skill:laws-enforcer` -> `laws-enforcer/SKILL.md`
- `skill:auto-loop-orchestrator` -> `auto-loop-orchestrator/SKILL.md`
- `skill:doc-loop-execution` -> `doc-loop-execution/SKILL.md`
- `skill:dev-loop-execution` -> `dev-loop-execution/SKILL.md`
- `skill:branch-management` -> `branch-management/SKILL.md`
- `skill:premerge-reconcile` -> `premerge-reconcile/SKILL.md`
- `skill:recovery-subagent-governance` -> `recovery-subagent-governance/SKILL.md`
- `skill:module-interface-governance` -> `module-interface-governance/SKILL.md`
- `skill:config-backup-guard` -> `config-backup-guard/SKILL.md`

Execution order (default):
1. `constitution-guard` (preflight gate)
2. `laws-enforcer` (acceptance gate)
3. domain workflow skill (`auto/doc/dev/branch`)
4. exception skill (`premerge-reconcile`) when needed
