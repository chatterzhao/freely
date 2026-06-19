# B1_IBM Brainstorm: ai-auth Template Configs

**raw-key**: 20260616T140126Z
**source**: chat-inbox
**created**: 2026-06-18

## Problem

New Freely users don't know how to configure `~/.ai-auth/` slots after installation. The slot naming convention (`{tool}-{type}-{name}`) and directory structure are not documented with working examples.

## Current State

- `~/.ai-auth/` slot system exists but has no template/example directory
- Users must reverse-engineer the convention from code comments or trial-and-error
- No `freely init` path that releases example configs

## Proposed Solution

Create `templates/ai-auth/` directory with example slot configurations:

### Templates

1. `claude-apikey-EXAMPLE/settings.json.example` — Claude API key mode with model config, env vars, permissions
2. `codex-account-EXAMPLE/config.toml.example` — Codex account mode with model, sandbox, approval policy
3. `opencode-apikey-EXAMPLE/settings.json.example` — OpenCode API key mode with provider config (API key stored externally)
4. `README.md` — Slot system overview, quick start, naming convention diagram, security notes
5. `zshrc-aliases.example` — Alias examples for all three tools

### `freely init` Integration

On `freely init`, copy `templates/ai-auth/` to `.freely/ai-auth/` and print setup hints.

### Documentation Alignment

Add cross-references from existing skill docs:
- `tool-config-matrix.md`
- `auth-setup.md`

## Open Questions

1. Should `freely init` always overwrite `.freely/ai-auth/` or only if absent?
2. Should templates support additional tools like `kiro-cli`?
3. Should `settings.json.example` include the full permission matrix or minimal safe defaults?

## Related Work

The recent ai-cli update added interactive login mode routing (`_prompt_generic_login_mode`, `_login_account_slot`, `_login_apikey_alias` with name prompting). Template examples should mirror these modes.
