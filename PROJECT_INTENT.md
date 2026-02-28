# Freely Project Intent

## Core Goal

Build a Jarvis-like autonomous loop runner:
- AI starts from project intent, not a fixed task list.
- AI self-manages brainstorm -> EPIC -> STORY -> implementation -> verification.
- AI keeps running continuously unless explicit stop conditions are met.

## Operating Model

1. Constitution-governed autonomy
- Constitution is the hard constraint surface.
- Branch/worktree rules, stack constraints, BMAD discipline, and external system constraints live in constitution.

2. Single active AI session per loop instance
- Each running instance owns one active AI CLI process/session.
- Monitoring targets that process/session lifecycle.

3. Recovery-first continuity
- Resume-first when tool supports non-interactive continuation.
- If resume cannot run in unattended mode, execute a bridge step:
  update progress docs with crash/blocking checkpoint, then restart unattended loop.

4. Minimal input surface
- Only four required inputs:
  - project absolute path
  - project intent path
  - constitution path
  - ai spec `tool:model:mode`
- AI discovers all other project docs by itself.

## Non-Goals

- Not a static backlog executor.
- Not a one-shot command runner.
- Not a human-driven ticket bot.
