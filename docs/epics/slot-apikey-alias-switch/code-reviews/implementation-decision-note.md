- issue_id: I-20260522T020249Z-A
## Implementation Decision Note
- decision: apikey slots use alias + config.env AI_TOOL, no tool-native file writes
- why_this: Slot dir holds settings file, alias points to it, runtime resolves via type→alias→settings chain
- alternatives_considered: Copy settings to tool dir (Codex-only, fragile), symlink (portability issues)
- residual_risk: Alias must exist in .zshrc before slot works; slot_create_apikey handles this
