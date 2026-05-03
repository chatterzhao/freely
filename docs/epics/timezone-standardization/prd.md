# PRD: Timezone Standardization

## Problem

The Freely system uses timestamps without timezone context across multiple locations. Different timezone users can produce conflicting timestamps. The system needs a single, unambiguous UTC+Z format.

## Requirements

1. All NEW timestamps use UTC+Z (ISO 8601 with Z suffix)
2. Existing timestamps in old format are accepted on read (backward compatible)
3. Format varies by context (keys: compact; logs: readable with separators)
4. One format specification, referenced by all generators

## Scope

### In scope
- Issue key format (raw-*, I-*, C-*)
- Branch/worktree naming convention
- Log timestamps in acp-bridge.py
- Doc metadata frontmatter format specification
- Tag version format
- Regex patterns in governance gates and scan scripts

### Out of scope
- Migrating existing issue directories (old names stay)
- SQLite data migration (old records keep their format)
- Platform API timestamps (GitHub/Gitee controlled)

## Format specification

Canonical: `YYYYMMDDThhmmssZ` — ISO 8601 with Z suffix

| Context | Format | Example |
|---------|--------|---------|
| Keys (issue/branch) | `YYYYMMDDThhmmZ` | `raw-20260503T0901Z` |
| Logs | `YYYY-MM-DDThh:mm:ssZ` | `2026-05-03T09:01:00Z` |
| Doc frontmatter | `YYYY-MM-DDThh:mm:ssZ` | `2026-05-03T09:01:00Z` |
| Tags | `YYYY.MM.DD-HHMMZ-stage` | `2026.05.03-0901Z-alpha` |
| Regex | `\d{8}T\d{4,6}Z` | matches both `T0901Z` and `T090100Z` |
