# Cross-shell alias resolution - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Replace hardcoded zsh with ${SHELL:-bash} for alias resolution. Works on zsh, bash, Linux, macOS. bash fallback for minimal systems.`
- why_this: `Only zsh aliases were resolved. Users on bash/Linux couldn't use custom aliases. $SHELL auto-detects user's shell.`
- alternatives_considered: `1) Config-based shell selection: rejected, adds config burden. 2) List all shells: rejected, slow. 3) $SHELL+fallback: chosen, POSIX standard.`
- boundary_non_goals: `No Windows PowerShell/fish support (freely runs in bash). AI_TOOL_FAMILY override available for edge cases.`
- residual_risk: `$SHELL may be unset on some systems; bash fallback handles this. Fish users need AI_TOOL_FAMILY override.`
