# Workspace

This directory is Freely's capability root for the current project.

Rules:
- Project governance always starts at `<project-root>/AGENTS.md`.
- This directory defines reusable Freely capabilities such as agents, skills, scripts, hooks, and runtime contracts.
- Do not duplicate project governance rules here; this directory should reference the project root `AGENTS.md` rather than maintain a second project entrypoint.
- When Freely develops itself, it still reads the repository root `AGENTS.md` first, then consumes capabilities from `docs/system/workspace/**`.
- The formal reusable contract for project-level `AGENTS.md` lives in `docs/system/workspace/project-agents-contract.md`.
