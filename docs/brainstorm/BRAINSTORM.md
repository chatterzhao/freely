# Brainstorm

## Context
Freely already has a bootstrap shell runner, but BMAD docs are mostly placeholders.
Several hard constitution constraints are not yet concretely implemented:
- local hook enforcement for `main` protection
- auto worktree creation flow for branch checkout in primary worktree
- explicit configuration backup behavior before overwrite

The first delivery must turn the repo from template state into a self-driving baseline.

## Options
1. Document-only first, defer tooling enforcement.
2. Document + minimal enforcement in scripts/hooks for immediate policy compliance.
3. Full runtime implementation in Rust/Tauri first, then backfill process controls.

## Tradeoffs
- Option 1: fast, but leaves hard constraints unenforced in daily workflows.
- Option 2: balanced; gives immediate guardrails and traceability with low change risk.
- Option 3: high engineering cost now, likely blocks autonomous loop progress.

## Decision
Choose Option 2 for STORY-001:
- complete BMAD decomposition
- add hook-based policy enforcement and installer
- add config backup logic to `bin/freely`
- validate script behavior and write review/progress/recovery artifacts

## Follow-up Actions
- [x] Define PRD scope and acceptance for governance baseline.
- [x] Decompose EPIC/STORY with territory and merge-path notes.
- [ ] Implement hooks + config backup + docs updates.
- [ ] Run script checks and write review record.
