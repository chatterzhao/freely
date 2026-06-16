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
created_at: '2026-06-15T23:58:34Z'
updated_at: '2026-06-15T23:58:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem
`.freely/config.env` uses shell `source` format (KEY="value"). Issues:
1. Only readable by shell — Python scripts parse manually, error-prone
2. No type safety — all values are strings
3. No structure — flat key=value, no nesting
4. `source config.env` executes arbitrary shell code — security risk

## Current state (June 2026)
- config.env still the only config format (no config.toml exists)
- `config_file()` returns `.freely/config.env` (freely line 1406)
- `global_config_file()` returns `~/.freely/config.env` (freely line 967)
- All runtime config reads go through `load_config` which sources the env file
- ACP bridge, session management, A2A task system all read from config.env

## Plan (backward compatible)

### Phase 1: TOML support (read + write)
1. Add `.freely/config.toml` as primary format
2. `load_config` reads config.toml first, falls back to config.env
3. `freely init` writes config.toml (not .env)
4. shell scripts read via `toml2env` helper (python3 -c "import tomllib...")

### Phase 2: Migration
5. On startup, if config.env exists but config.toml doesn't → auto-migrate
6. Keep config.env as fallback for 1 release cycle

### Phase 3: Deprecation
7. Remove config.env support after migration period
8. All Python scripts use tomllib directly

## Acceptance
- [ ] config.toml as primary format
- [ ] Old config.env still readable (backward compat)
- [ ] Python scripts use tomllib
- [ ] Shell scripts use toml2env helper
- [ ] freely init generates config.toml
- [ ] Auto-migration from config.env on startup
