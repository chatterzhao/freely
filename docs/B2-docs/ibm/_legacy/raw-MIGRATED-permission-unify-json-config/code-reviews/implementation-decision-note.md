- issue_id: I-20260521T135911Z-A
- issue_path: docs/issues/I-20260521T135911Z-A/issue.md
## Implementation Decision Note
- decision: Remove all permission flags from bridge and aliases, rely on JSON config native permission fields
- why_this: bypassPermissions is Claude-specific; opencode doesn't recognize it causing Internal error. JSON config is the single source of truth each tool reads natively.
- alternatives_considered: Keep bridge injecting mode per-tool (adds complexity), keep alias flags (deprecated)
- boundary_non_goals: Not changing .zshrc or user settings JSON files (user-managed)
- residual_risk: Users must add defaultMode/permission to their JSON configs
