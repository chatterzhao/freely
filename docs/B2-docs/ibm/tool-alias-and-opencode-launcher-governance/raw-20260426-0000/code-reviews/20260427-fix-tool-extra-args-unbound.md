# Fix tool_extra_args unbound variable - verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Replace ${tool_extra_args[@]} with ${tool_extra_args[@]:-} in all exec lines. Fixes unbound variable error under set -u when AI_TOOL_EXTRA_ARGS is not configured.`
- why_this: `Daemon cycle failed with "unbound variable" on line 405. The empty array expansion triggers set -u on macOS bash 3.2.`
- alternatives_considered: `1) Remove set -u: rejected, it catches real bugs. 2) Always initialize array with a dummy value: rejected, adds noise. 3) Use :- default: chosen, clean and standard.`
- boundary_non_goals: `No behavior change. No new features.`
- residual_risk: `None. Fix is backward compatible.`
