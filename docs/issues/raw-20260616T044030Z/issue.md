---
local_id: raw-20260616T044030Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2815'
    url: https://github.com/chatterzhao/freely/issues/2815
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T04:40:46Z'
updated_at: '2026-06-16T09:28:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Requirements (complete, no fallback)

Phase 1 implemented backward-compatible config.env fallback. This issue
requires COMPLETE migration with NO config.env dependency.

### 1. Remove all config.env fallback
- freely_config.py: remove parse_env_file(), only read config.toml
- All shell scripts: use toml2env exclusively, never source config.env
- Delete fallback paths in freely, ai-cli, monitor-ai-acp.sh

### 2. Verify ALL call sites
Check every file that reads config:
- docs/system/workspace/scripts/runtime/freely
- docs/system/workspace/scripts/runtime/ai-cli
- docs/system/workspace/scripts/runtime/monitor-ai-acp.sh
- docs/system/workspace/scripts/runtime/tool-launchers.sh  
- docs/system/workspace/scripts/runtime/acp-bridge.py
- docs/system/workspace/scripts/runtime/signal-intent-handler
- docs/system/workspace/scripts/runtime/interruption-manager-handler
- docs/system/workspace/scripts/runtime/network-proxy-resolver.sh
- bin/freely (wrapper)

### 3. Create config.toml template
- Default config.toml with all fields documented
- freely init generates config.toml

### 4. Migration
- On startup: if config.env exists but config.toml doesn't → auto-migrate once
- After migration: remove or rename config.env

### 5. Acceptance
- [ ] No source of config.env anywhere
- [ ] config.toml template exists
- [ ] freely init creates config.toml
- [ ] All call sites verified
- [ ] Auto-migration from old config.env
