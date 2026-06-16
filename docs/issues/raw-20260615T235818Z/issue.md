---
local_id: raw-20260615T235818Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2780'
    url: https://github.com/chatterzhao/freely/issues/2780
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T23:58:18Z'
updated_at: '2026-06-15T23:58:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

feat: config.env -> config.toml — Freely project config from shell-source to TOML

## Problem
.freely/config.env uses shell source format. Only readable by shell,
no type safety, no structure, security risk from source execution.

## Plan
Phase 1: Add config.toml support with backward compat
Phase 2: Auto-migrate from config.env on startup
Phase 3: Deprecate config.env after migration period

## Acceptance
- config.toml as primary format
- Old config.env still readable
- Python scripts use tomllib
- Shell scripts use toml2env helper
- freely init generates config.toml
