# Brainstorm: ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance

## Decision

`ai-switch-cli` remains the intended long-term backend direction, but extraction does not start merely because a local skeleton repo exists. Freely remains canonical until a future owner can prove the extraction-start checklist is satisfied and can move a backend-owned slice without reopening threshold research.

## Why This

1. Codex is now strong enough to prove the backend direction is real.
2. Only Codex currently has verified save/switch/probe/materialization truth, so splitting immediately would duplicate unstable tool-private knowledge.
3. The local `codex-account-switch` repo is still disposable scaffolding with old naming and no commits, so it cannot be treated as backend truth.

## Extraction-Start Package

The future extraction owner must consume this package before opening any standalone repo lane:

1. `issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
2. `prd.md`
3. `pre-tests.md`
4. `tasks.md`
5. `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/raw-20260405-0027issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`

## Start Checklist

All of the following must be true:

1. command surface and JSON envelope are already frozen enough for Freely to consume via CLI/JSON only
2. at least one tool still has verified save/switch/probe/materialization truth
3. generic helpers needed for backend life, especially backup-before-write and generic slot inventory surfaces, are no longer just inline tool-local fragments
4. the first move is scoped to backend-owned surfaces and does not drag Freely orchestration policy into the new repo
5. the repo path decision is explicit:
   - `rename_in_place`
   - `fresh_repo`

## Repo Disposition Rule

The current local skeleton may follow one of two paths:

1. `rename_in_place`
   - allowed only once extraction formally starts
   - rename to `ai-switch-cli` before the first real commit
   - rewrite top-level naming truth before any backend implementation is declared canonical
2. `fresh_repo`
   - preferred if the current skeleton contains only boilerplate or stale naming risk
   - no future owner may justify reuse solely because the directory already exists

## Boundary Summary

Freely keeps:

1. project-level priority ordering
2. watchdog retry and recovery policy
3. init-time backend detection and project-local UX
4. tool orchestration across providers

Backend keeps:

1. login/save/delete/switch implementation
2. tool-specific config mutation
3. probe execution
4. machine-readable JSON output

## Non-Goals

1. no standalone packaging or installer work in this owner
2. no migration of current `ai-cli` code in this owner
3. no claim that non-Codex tools already reached parity
