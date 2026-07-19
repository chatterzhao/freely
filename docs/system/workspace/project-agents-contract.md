# Project-Level AGENTS Contract

This document freezes Freely's first reusable contract for project-level `AGENTS.md`.

## Contract

1. `<project-root>/AGENTS.md` is the project governance entrypoint.
2. Runtime and manager/worker flows must read `<project-root>/AGENTS.md` before they consume reusable Freely capability docs under `docs/system/workspace/**` or helper commands under `bin/**`.
3. `freely init` creates a minimal project-level `AGENTS.md` only when the target project does not already have one.
4. If the target project already owns `AGENTS.md`, Freely preserves it; this first contract slice does not overwrite, merge, or upgrade that file.
5. The generated minimal file is only a bootstrap entrypoint. It is not a substitute for a project-maintained `AGENTS.md`, and it is not the same layer as this repository's hand-maintained root `AGENTS.md`.
6. When Freely develops itself, it still follows the same contract: read the repository root `AGENTS.md` first, then consume reusable capability truth from `docs/system/workspace/**`.

## First-Slice Boundary

This slice intentionally does not define:

- richer generated templates
- project-intent summary injection
- auto-upgrade or merge flows for existing `AGENTS.md`
- interactive migration or conflict resolution

Those behaviors require a separate follow-on owner.
