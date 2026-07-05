# Brainstorm: AI_TOOL alias type-based resolution

## Context
Freely\'s AI_TOOL configuration sometimes fails when alias names like `cc-ai98pro-0045-auto` don\'t resolve correctly. The current implementation uses `alias` command which is fragile and shell-dependent.

## Problem Analysis
1. `_resolve_tool_family` uses `${SHELL} -ic "alias"` — only works for aliases, not functions/binaries
2. `_apply_tool_alias_settings` uses same fragile pattern + has Python f-string bug
3. Hardcoded prefix lists needed for each new alias pattern

## Decision
Use `type` command instead of `alias`. `type` works for aliases, functions, and binaries uniformly across zsh/bash. Extracted expansion directly gives binary name (claude, codex, opencode, etc.) which IS the tool family.

## Alternatives
1. Keep `alias` + add more hardcoded prefixes — fragile
2. Use `whence` (zsh-only) — not portable
3. Use Python-based shell detection — over-engineered

## Selected: type-based resolution
- One `_resolve_type_expansion` helper handles zsh/bash format differences
- Binary name = tool family (no arbitrary mapping)
- One-level recursive resolution for alias chains
- Also fix `bin/deploy-skills` cc* → ~/.claude/skills
