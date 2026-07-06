# Fix worker prompt extraction - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Normalize AI-written section headers to canonical names. Accept any line containing worker prompt path pattern (not just list-item format). Add rg-based fallback in csv_from_continuity.`
- why_this: `The awk extraction function has two format assumptions that didn't match AI output: exact section name "worker prompts" (AI writes singular/variations) and list-item line format "- /path" (AI writes "See: /path"). This caused 150+ worker prompts to accumulate without ever being dispatched.`
- alternatives_considered: `1) Fix AI prompt to write exact format: rejected, fragile. 2) Only fix section names: insufficient, line format also mismatched. 3) Fix both + rg fallback: chosen, robust.`
- boundary_non_goals: `No changes to worker prompt content or dispatch flow. Only extraction.`
- residual_risk: `rg fallback might find stale paths from older sections. Mitigated by preferring structured extraction first.`

## Verification
- bash -n: `pass`
- "## Worker Prompt" (singular) with "See: /path" format: `pass` (path extracted)
- "## Worker Prompts" (plural) with list-item format: `pass` (unchanged, still works)
- rg fallback when awk returns empty: `pass`
