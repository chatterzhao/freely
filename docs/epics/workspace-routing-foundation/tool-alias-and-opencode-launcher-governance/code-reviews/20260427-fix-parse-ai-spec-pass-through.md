# Fix parse_ai_spec pass-through - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Change parse_ai_spec to pass through unknown tools with a warning instead of erroring and exiting. Add claude to known list.`
- why_this: `The hard whitelist rejected alias-based tools like cc-ds-auto before _resolve_tool_alias could run. start-lead-agent.sh already had the correct pass-through behavior.`
- alternatives_considered: `1) Add cc-ds-auto to whitelist: rejected, doesn't scale for arbitrary aliases. 2) Remove check entirely: rejected, mode validation still useful. 3) Warn + pass through: chosen, matches start-lead-agent.sh.`
- boundary_non_goals: `No changes to downstream alias resolution. No changes to tool-launchers.sh (already handles claude).`
- residual_risk: `Truly mistyped tool names will be caught later (exec fails).`

## Verification
- bash -n: `pass`
- parse_ai_spec with cc-ds-auto: `pass` (warns, passes through)
- parse_ai_spec with claude: `pass` (matched by known list)
- parse_ai_spec with codex: `pass` (unchanged behavior)
