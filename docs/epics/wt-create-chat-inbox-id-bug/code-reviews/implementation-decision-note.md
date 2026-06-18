# Implementation Decision Note

## Decision

Normalize chat-inbox ID by stripping TZ characters with `tr -d 'TZ'` before passing to `chat-inbox.py` commands.

## Why This

- Minimal change: 4 lines modified, all following the same pattern already used by SQL queries in the same functions
- Consistent: the existing SQL queries already compute `ts_bare` correctly; the bug was that `chat-inbox.py` calls didn't use it
- Chat-inbox.py expects bare IDs (its help text says `YYYYMMDDHHMMSS`)

## Alternatives Considered

1. **chat-inbox.py handles both formats**: Would require changing the Python script to accept either format, increasing complexity and testing surface
2. **Store IDs with TZ in DB**: Would break existing data and require migration

## Boundary / Non-Goals

- Does not change chat-inbox.py interface
- Does not modify DB schema
- Does not affect `--source platform` or `--source local` paths

## Residual Risk

- If future code adds new `chat-inbox.py` call sites, they may also forget to normalize. Mitigation: grep for `--id.*\$ts` patterns in reviews.
