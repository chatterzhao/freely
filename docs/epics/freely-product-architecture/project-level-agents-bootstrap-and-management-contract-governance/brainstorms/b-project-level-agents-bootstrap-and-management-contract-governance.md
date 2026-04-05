# Brainstorm: project-level-agents-bootstrap-and-management-contract-governance

## Focus

Freeze the first reusable capability contract for project-level `AGENTS.md` without widening into template customization or migration tooling.

## Narrowing Decisions

1. The first slice only formalizes the existing behavior: create when missing, preserve when present, read project root first.
2. The first slice adds a focused regression rather than redesigning runtime logic.
3. Self-hosting is documented as the same contract, not a second special-case system.
4. Richer generation/update behavior remains a follow-on topic.
