# Brainstorms

## Discovery

- **Source**: Manager auto-loop continuity analysis from 2026-06-18 session
- **Problem**: wt-create `--source chat-inbox` worktree creation fails because `chat-inbox.py` commands (`show`, `materialize`, `consume`) receive `$ts` with TZ characters (`Z`, `T`) but the SQLite DB stores bare numeric IDs (`YYYYMMDDHHMMSS` without separators)
- **Scope**: 4 call sites across 3 functions (`_pull_raw_issue`, `_require_issue_exists`, `_materialize_chat_if_needed`)

## Research

- `chat-inbox.py` `cmd_show` help explicitly states `--id` format is `YYYYMMDDHHMMSS` (bare)
- 3 of 4 call sites computed `$ts_bare` via `tr -d 'TZ'` for SQL queries but used `$ts` for `chat-inbox.py` commands
- The 4th site (`_require_issue_exists` chat-inbox case) didn't have `ts_bare` at all
- Fix is mechanical: replace `--id "$ts"` with `--id "$ts_bare"` at all 4 sites

## Decision

This is a straightforward bug fix with no open design questions. No research-phase issues remain. Promote directly to absorbed.
