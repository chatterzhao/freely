# PRD: ai-auth Template Config Files

**I-20260616T140126Z-A** | **Epic**: ai-auth-template-config

## Problem Statement

New Freely users cannot configure `~/.ai-auth/` slots without reverse-engineering the naming convention from code. No working examples exist.

## Slot Naming Convention

`{tool}-{type}-{name}` where:
- `{tool}` = claude | codex | opencode | cc | kiro-cli
- `{type}` = apikey | account
- `{name}` = user-defined slot name

Freely identifies tool families by `-apikey-` / `-account-` prefix in the directory name.

## Scope

### In Scope
1. `templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example`
2. `templates/ai-auth/codex-account-EXAMPLE/config.toml.example`
3. `templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example`
4. `templates/ai-auth/README.md` — slot system overview
5. `templates/ai-auth/zshrc-aliases.example`
6. `freely init` — copy templates to `.freely/ai-auth/`
7. Cross-reference updates in skill docs

### Out of Scope
- Default slot creation during `freely init`
- Interactive slot setup wizard
- kiro-cli / cc template examples (future)
- Migration of existing slots
- Validation of user slots against templates

## Design Decisions

1. **Overwrite on re-init**: Always overwrite `.freely/ai-auth/` on `freely init` (templates are small and deterministic)
2. **API key placeholder**: Use `your-apikey` consistently across all examples
3. **Permission defaults**: Bypass permissions mode by default; users customize for production

## Files

### claude-apikey-EXAMPLE/settings.json.example
- model: claude-opus-4-8
- env: ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, model overrides
- permissions: bypassPermissions with allow/deny lists
- hooks: pre/post/onFailure stubs
- theme: dark, editor: vim

### codex-account-EXAMPLE/config.toml.example
- model, sandbox, approval_policy, writable_roots
- provider_id, auto_approve settings

### opencode-apikey-EXAMPLE/settings.json.example
- model, provider config
- Note: opencode API key stored externally, not in settings.json

## Dependencies

- `freely init` command needs update to add template release step
- Existing skill docs (tool-config-matrix.md, auth-setup.md) need cross-reference update
