# Agent Context Entry

## Authoritative Sources (in order)
1. `docs/CONSTITUTION.md` (hard constraints)
2. `docs/LAWS.md` (operational rules)
3. `docs/PROJECT_INTENT.md` (product direction)
4. `AGENTS.md` (entry guidance only, must not override 1-3)

If any statement in this file conflicts with the three core docs above, the core docs win.

## Current Project Phase
Freely is in a research-first consolidation phase.
Current active docs scope is:
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/PROJECT_INTENT.md`
- `docs/pre-brainstorms/`

Do not treat legacy paths as active workflow inputs (for example: `docs/brainstorms/`, `docs/planning/`, `docs/continuity/`, `docs/validation/`, `docs/reviews/` under old layout).

## Dogfooding Rule (Freely builds Freely)
Freely must be developed under Freely governance rules, without project-specific exceptions.

Required:
- Use the same branch/worktree/hook discipline expected for user projects.
- Worktree root follows constitution policy: project sibling directory named `{project-name}-worktrees`.
- Architecture/governance changes must first enter `docs/pre-brainstorms/<id>/` before execution-loop landing.
- Prefer preflight checks + actionable remediation over repeated privilege prompts.

## Execution Guidance
- Keep this file minimal and stable; do not duplicate detailed rules from Constitution/Laws.
- Add details to the canonical docs, then reference them here.
- When uncertainty appears, open/update a pre-brainstorm entry and converge there first.

## Minimal Commands
- `./bin/freely init|doctor|start|status|stop`
- `./bin/bmad-check`
- `./bin/test-pre-push-hook`
- `source ./bin/wt-enter <branch>`
- `source ./bin/wt-add <branch> -- <git-add-args>`
