# B2 Brainstorm: Timezone Standardization

## Context

GitHub #179: standardize timezone rendering. The B1 brainstorm (docs/pre-brainstorms/20260503-0901--timezone-standardize/) converged on UTC+Z format. Now implementing across 7 locations.

## Key decisions

### Format: UTC+Z, not +HH:MM offset

The issue originally proposed `+08:00` offset format, but the B1 design converged on `Z` (UTC). This is simpler, unambiguous, and avoids DST confusion. All internal timestamps are UTC; display conversion is the UI layer's responsibility.

### Backward compatibility model

Old format (`YYYYMMDD-HHMM`) is accepted everywhere on read. Only NEW key generation uses the new format. Existing directory names, tags, and SQLite records are unchanged. This avoids a migration that touches every past issue directory.

### The `T` separator and `Z` suffix are part of the key

Unlike the old format where `YYYYMMDD-HHMM` was the key (a simple string), the new key `YYYYMMDDThhmmZ` embeds structural characters. All key extraction functions must match both: `\d{8}-\d{4}` and `\d{8}T\d{4,6}Z`.

### SQLite: already correct

The `chat-inbox.py`, `session-store.py`, and `task-source-scan.py` all already generate `YYYY-MM-DDThh:mm:ssZ`. No change needed. Only `acp-bridge.py` was missing the `Z`.

## Per-file change summary

| File | Change |
|------|--------|
| `acp-bridge.py:72` | Add `Z` to `time.strftime` format |
| `task-lifecycle-scan.py` | Add `\d{8}T\d{4,6}Z` to all key regex patterns |
| `governance-merge-gate` | Add `T\d{4,6}Z` variant to branch/issue key regexes |
| `wt-create` | Add `T\d{4,6}Z` variant to `_extract_issue_key` |
| `CONSTITUTION.md §3` | Change `HHMM-stage` to `HHMMZ-stage` |
| `ibm-framework.md` | Update ID format references |
