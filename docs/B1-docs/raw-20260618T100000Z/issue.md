---
local_id: raw-20260618T100000Z00Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T100000Z-A
platform_ids: {}
primary_platform: ''
platform_state: closed
---
## Problem

`wt-create` script has a chat-inbox ID normalization bug at 3 call sites:
`_pull_raw_issue` (lines 309, 313) and the pre-creation validation (line 451)
pass `--id "$ts"` (with TZ chars like `Z`) to `chat-inbox.py`, but the DB
stores IDs as bare numeric (e.g. `20260616140126` vs `20260616T140126Z`).

Lines 294, 493 correctly compute `ts_bare=$(echo "$ts" | tr -d 'TZ')` and use
it for SQL queries, but the `materialize` and `consume` calls still use `$ts`.

## Fix

Replace `--id "$ts"` with `--id "$ts_bare"` at lines 309, 313, and 451.
