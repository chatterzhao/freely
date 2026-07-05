---
local_id: raw-20260627T030447Z47Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3578'
    url: https://github.com/chatterzhao/freely/issues/3578
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T030447Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T03:05:08Z'
updated_at: '2026-06-27T03:05:08Z'
intake_id: ''
author: zhaoquan
channel: github
session_refs: []
---

## Root Cause

1. `tool_supported_adapters_for_runtime()` hardcodes supported adapters: only `codex` and `opencode` have `acp` support. `claude` and `cline` fall through to the default case (direct only), despite tool-registry.toml declaring ACP support.

2. `tool_default_adapter()` always returns `direct`, ignoring registry `adapters.default`.

3. `AI_TOOL_ADAPTER` env var not exported for monitor script dispatch.

## Changes

- `freely`: Add `claude`/`cline` to `tool_supported_adapters_for_runtime()` ACP case
- `freely`: Make `tool_default_adapter_for_runtime()` registry-driven
- `freely`: Export `AI_TOOL_ADAPTER` after computing
- `tool-launchers.sh`: Make `tool_default_adapter()` registry-driven
