# File size tip - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add FILE_SIZE_TIP threshold (default 300 lines) as a proactive refactoring hint below WARN. Output [TIP] prefix in check-file-size.`
- why_this: `Early awareness of growing files gives maintainers a nudge before the file reaches WARN. Configurable via FILE_SIZE_TIP env var.`
- alternatives_considered: `1) Two-level only (WARN/ERROR): rejected, too coarse for proactive maintenance. 2) Per-directory thresholds: rejected, over-complicated. 3) Three-level TIP/WARN/ERROR: chosen, simple and effective.`
- boundary_non_goals: `No gate enforcement at TIP level (advisory only). No per-file override for TIP (uses global config).`
- residual_risk: `Users may ignore TIP output if too noisy. Mitigated by configurable threshold.`

## Verification
- bash -n: `pass`
- execution: `pass` (4 TIPs, 6 WARNs, 0 ERRORs shown with default limits)
- skip markers: `pass` (skip markers tested in PT-33, unaffected by this change)
- config override: `pass` (FILE_SIZE_TIP can be set in .freely/config.env, defaults to 300)
