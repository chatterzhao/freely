# ai-auth Slot Configuration

This directory contains example slot configurations for Freely's `~/.ai-auth/` authentication slot system.

## Slot Naming Convention

```
{tool}-{type}-{name}
  tool = claude | codex | opencode | cc | kiro-cli
  type = apikey | account
  name = your custom slot name (e.g., personal, work, EXAMPLE)
```

The slot directory name, `.zshrc` alias, and `config.toml` `AI_TOOL` value **must all match**.

## Quick Start

### 1. Choose Your Tool

| Tool | Auth Mode | Example |
|------|-----------|---------|
| Claude (claude-code) | `apikey` | `claude-apikey-personal` |
| Codex | `account` | `codex-account-work` |
| OpenCode | `apikey` | `opencode-apikey-default` |

### 2. Copy & Customize

```bash
# Claude API key example
cp -r templates/ai-auth/claude-apikey-EXAMPLE ~/.ai-auth/claude-apikey-personal
# Edit settings.json, replace your-apikey with your real key

# Codex account example
cp -r templates/ai-auth/codex-account-EXAMPLE ~/.ai-auth/codex-account-work
# Edit config.toml, replace your-apikey

# OpenCode example
cp -r templates/ai-auth/opencode-apikey-EXAMPLE ~/.ai-auth/opencode-apikey-default
# Set OPENCODE_API_KEY in your environment
```

### 3. Add Shell Alias

Source the aliases or add to your `.zshrc`:

```bash
source templates/ai-auth/zshrc-aliases.example
```

## Safety Notes

- **Never commit real API keys** — use `your-apikey` placeholder
- Slot directories are local to your machine
- Use separate slots for different projects or auth scopes
- Review permissions in each template before use
