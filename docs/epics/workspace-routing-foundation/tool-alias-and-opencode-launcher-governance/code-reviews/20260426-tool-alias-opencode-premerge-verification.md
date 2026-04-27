# tool-alias-and-opencode-launcher - premerge verification

- owner_issue: `I-20260426-0000-A`
- verified_at: `2026-04-26`
- status: pass

## Decision

Add opencode direct launcher and shell alias resolution to tool-launchers.sh. Users set AI_TOOL to any shell alias name; freely resolves via zsh and detects tool family from the resolved binary.

## Why This

codex API balance is exhausted. Users need to switch to other tools (opencode, ccds alias) without modifying freely code. Alias resolution lets users control model/settings/auth entirely in their shell config.

## Alternatives Considered

1. Per-alias hardcoded cases: rejected because it requires freely code changes for every new alias.
2. Full generic launcher without tool families: rejected because resume/session conventions differ per tool.
3. AI_TOOL_EXTRA_ARGS only (no alias resolution): rejected because users want to use their existing alias names directly.

## Boundary Non-Goals

- No auto-detection of session patterns from tool output
- No removal of existing tool family cases (backward compatible)
- No opencode slot/switch parity with codex

## Residual Risk

- Alias resolution via zsh -ic may fail if .zshrc has side effects. Mitigated: AI_TOOL_FAMILY override.
- Session ID extraction for opencode depends on --print-logs format stability.

## PT-1: opencode launch
Launched via daemon: ai_launch_begin tool=opencode tool_adapter=direct launch_kind=fresh.

## PT-2: Session ID extraction
Pattern matches ses_* from --print-logs. Tested with ses_233722117ffeOuUkPrDjl06elo.

## PT-3: ccds alias resolution
zsh -ic "alias ccds" returns claude --settings ~/.claude/settings_deepseek.json.
Binary claude detected, enters cc family.

## PT-4: AI_TOOL_EXTRA_ARGS injection
--settings flag appears before freely-managed flags in exec line.
