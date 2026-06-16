# Brainstorm: config.env → config.toml Complete Migration

## Discovery

### Current state (post-Phase 1+2 partial merge)
- `config_file()` returns `.freely/config.toml` (changed)
- `load_config()` reads config.toml only — exits if missing
- `interruption-manager-handler` exits if config.toml missing
- `signal-intent-handler` exits if config.toml missing
- `.freely/config.toml` does NOT exist → daemon can't start
- Phase 1 backward-compatible code was removed in Phase 2
- `freely_config.py` has full TOML read/write support

### What config.env contains (56 keys)
PROJECT_ROOT, INTENT_FILE, CONSTITUTION_FILE, FREELY_HOME,
AI_TOOL, AI_MODEL, AI_MODE, AI_REASONING_EFFORT,
AI_TOOL_ADAPTER, AI_TOOL_ADAPTER_POLICY, AI_TOOL_CAPABILITIES,
AI_TOOL_POLICY, + codex capability settings

### Files that reference config
See analysis comment on #2815: freely, ai-cli, monitor-ai-acp.sh,
tool-launchers.sh, signal-intent-handler, interruption-manager-handler,
freely_config.py, bin/freely

## Research

### Approach A: Full revert to config.env
- Pro: daemon works immediately
- Con: loses TOML benefits, regression

### Approach B: Auto-migration on startup (chosen)
- load_config() tries config.toml first
- If missing: reads config.env, creates config.toml, logs migration
- If config.toml exists: uses it directly
- config.env kept as fallback for 1 release cycle
- freely_config.py `init-toml` command for explicit migration

### Approach C: Manual migration script
- Pro: explicit control
- Con: daemon can't self-heal, requires human intervention

## Decision

**Approach B** — auto-migration in load_config().

load_config already has `source_config()` that reads TOML via toml2env.
Add fallback: if config.toml missing but config.env exists → auto-migrate.
Then freely init generates config.toml directly.

### Backward compatibility
- If both exist: use config.toml (newer format)
- If only config.env: auto-migrate to config.toml, then use it
- If only config.toml: use directly
- If neither: error (project not initialized)

### .gitignore
- `.freely/` already gitignored — config.toml is NOT tracked
- config.toml.example should be tracked in repo root
