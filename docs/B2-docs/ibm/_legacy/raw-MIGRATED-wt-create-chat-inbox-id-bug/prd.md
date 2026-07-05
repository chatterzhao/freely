# PRD: wt-create chat-inbox ID normalization

## Goal

Fix wt-create so `--source chat-inbox` worktree creation works end-to-end.

## Background

When creating a worktree with `--source chat-inbox`, wt-create calls `chat-inbox.py` commands (`show`, `materialize`, `consume`) with `--id $ts` where `$ts` contains TZ characters (e.g. `20260618T100000Z`). The DB stores bare numeric IDs (`202606181000000`), so the SQL `WHERE id=?` query fails to match.

## Dev-Loop Handoff

The fix has already been implemented and committed (`1f6a60340`). The remaining work is governance documentation (this B2_IBM cycle), followed by PR creation and merge.
