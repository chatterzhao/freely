# tool-alias-and-opencode-launcher - premerge verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Add opencode direct launcher case and shell alias resolution to tool-launchers.sh. Users set AI_TOOL to any shell alias name; freely resolves via zsh and detects tool family from the resolved binary.`
- why_this: `codex API balance exhausted. Users need to switch tools without modifying freely code. Alias resolution lets users control model/settings/auth entirely in their shell config.`
- alternatives_considered: `1) Per-alias hardcoded cases: rejected (requires code change per alias). 2) Full generic launcher without tool families: rejected (resume/session conventions differ). 3) AI_TOOL_EXTRA_ARGS only: rejected (users want to use alias names directly).`
- boundary_non_goals: `No auto-detection of session patterns. No removal of existing tool family cases. No opencode slot/switch parity with codex.`
- residual_risk: `Alias resolution via zsh -ic may fail if .zshrc has side effects (mitigated by AI_TOOL_FAMILY override). Session ID extraction depends on --print-logs format stability.`

## PT-1: opencode launch
Launched: ai_launch_begin tool=opencode tool_adapter=direct launch_kind=fresh.

## PT-2: Session ID extraction
Pattern ses_* matched: ses_233722117ffeOuUkPrDjl06elo extracted from --print-logs.

## PT-3: ccds alias resolution
zsh -ic resolves ccds to claude --settings ~/.claude/settings_deepseek.json. Binary claude detected, enters cc family.

## PT-4: AI_TOOL_EXTRA_ARGS injection
Extra args appear before freely-managed flags in exec line.
