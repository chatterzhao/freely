# PRD

## Problem
Freely cannot yet operate as a constitution-compliant autonomous loop baseline because:
- BMAD artifacts are placeholders and not actionable.
- Worktree/hook governance is partially implied but not fully enforced.
- Configuration overwrite path lacks backup safeguards required by constitution.

## Goals
1. Produce a complete, executable BMAD baseline from brainstorm to active stories.
2. Enforce local Git governance minimums:
- block pushes that target `main`
- auto-create branch worktree when branch checkout occurs in primary worktree
3. Ensure runtime config rewrite in `bin/freely` creates timestamped backup first.
4. Keep flow traceable: Intent -> PRD -> EPIC -> STORY -> Code/Test -> Review/Progress.

## Scope
In scope:
- `docs/brainstorm/BRAINSTORM.md`, `docs/PRD.md`, `docs/EPIC.md`, `docs/STORY.md`
- `docs/PROGRESS.md`, `docs/RECOVERY.md`, one new `docs/review/*`
- `bin/freely` config backup enhancement
- repository-managed git hooks and installer script
- README runbook update for hook/worktree governance

Out of scope:
- Tauri/Rust/React runtime modules (future EPIC)
- release/hotfix automation
- CI pipeline integration

## Non-Goals
- Build the full Jarvis loop runtime in this story.
- Replace shell bootstrap with Rust service in this iteration.
- Automate merging into `develop` or `main`.

## Acceptance
1. No `<TBD>` placeholders remain in core BMAD runtime docs.
2. `bin/freely` backs up existing `config.env` before overwrite with unique timestamp suffix.
3. Hooks exist in repo, can be installed with one command, and enforce:
- no pushes targeting `main`
- auto worktree creation behavior for feature/release/hotfix checkout in primary worktree
4. Script syntax validation and basic behavior checks pass.
5. Progress, recovery, and review documents record branch/worktree and verification results.
