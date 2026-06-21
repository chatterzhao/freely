## C-20260621T130954Z-A

- **Action**: Fix `a2a_task.py` — change `latest_manager()`, `pending_delivery()`, `launched_pids()` from `_request` to `_rest_request`
- **Status**: promoted
- **Owner**: `I-20260621T130954Z-A`
- **Effort**: trivial (3 lines, 1 file)
- **Risk**: minimal (same pattern as `list()`, `create()`, `update()`)
- **Verification**: daemon start → `latest-manager` returns correct dict → workers launch
