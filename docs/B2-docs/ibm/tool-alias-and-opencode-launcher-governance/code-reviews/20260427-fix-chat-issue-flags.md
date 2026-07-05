# Fix cmd_chat issue flag parsing - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add --issue/--new-issue/--urgent flag parsing to cmd_chat(), forward them through submit_human_frontdoor_message() to cmd_intake_chat(). Default to --new-issue when neither is specified.`
- why_this: `cmd_chat() documented these flags in usage text but never parsed them, breaking all human chat intake. Internal callers (TUI, restore-work) also broke when --issue/--new-issue became required.`
- alternatives_considered: `1) Require flags for all callers: rejected, breaks TUI/restore-work. 2) Only fix cmd_chat(): rejected, TUI would break. 3) Fix cmd_chat + default --new-issue: chosen, backward compatible.`
- boundary_non_goals: `No changes to cmd_intake_chat() issue routing logic.`
- residual_risk: `None — additive fix that only affects entry-point parsing.`

## Verification
- bash -n: `pass`
- cmd_chat --issue I-xxx "msg": `pass` (parses correctly)
- cmd_chat --new-issue "msg": `pass` (sets new_issue=true)
- cmd_chat "msg" (no flags): `pass` (defaults to --new-issue)
- TUI submit_human_frontdoor_message: `pass` (no flags, defaults to --new-issue)
