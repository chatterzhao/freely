# Auto-detect tool family - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add _resolve_tool_family() that resolves aliases to known binaries. All tool classification functions use it. No more whitelist additions needed.`
- why_this: `Every new alias required code changes to whitelists. Now cc-ds-auto, ccglm, or any future alias auto-detects as claude via zsh resolution.`
- alternatives_considered: `1) Config-based family mapping: rejected, adds config burden. 2) Prefix matching (cc-*): rejected, fragile. 3) Alias resolution: chosen, zero-config, uses existing alias definitions.`
- boundary_non_goals: `No AI_FAMILY override removal (still available for edge cases).`
- residual_risk: `Alias resolution depends on zsh -ic. If user's shell is different, override with AI_TOOL_FAMILY.`
