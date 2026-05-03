## Issue
GitHub #179 — standardize timezone rendering across the entire system

## Problem
Current system uses timestamps without timezone context. Multiple places:
- Issue keys: raw-YYYYMMDD-HHMM (no tz)
- Branch names: feature/raw-YYYYMMDD-HHMM-slug (no tz)
- Logs: acp-bridge.py mixed formats, no tz
- Doc metadata: frontmatter created_at/updated_at inconsistent
- Tags: YYYY.MM.DD-HHMM-stage (no tz)
- SQLite: sessions/chats created_at format needs confirmation

## Design
UTC+Z format: YYYYMMDDThhmmssZ (ISO 8601 with Z suffix)

Per-context format:
- Keys/tags: YYYYMMDDThhmmZ (no seconds)
- Branches: raw-YYYYMMDDThhmmZ-slug
- Logs/metadata: YYYY-MM-DDThh:mm:ssZ (readable with separators)
- Regex: \d{8}T\d{4,6}Z

## Requirements
1. Backward compatible — old \d{8}-\d{4} still recognized
2. All 7 locations covered (see issue)
3. Format specification in one place, referenced by all generators

## Acceptance Items
- AI-generated keys use new format
- Log timestamps show tz
- Doc frontmatter updated
- Existing data preserved (no migration needed, accept old format on read)

## Next
Progress to B2 IBM: document each location's specific changes, write pre-tests.
