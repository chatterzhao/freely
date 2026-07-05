# AGENTS.md break-glass guidance hardening - post-merge verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Harden AGENTS.md line 114 to explicitly list forbidden break-glass patterns and narrow verified_false_negative to factual errors only.`
- why_this: `Two break-glass bypasses occurred during I-20260426-0000-A dogfooding. The old soft guidance ("若确实命中") contributed to AI rationalization.`
- alternatives_considered: `1) Change LAWS.md §2D directly: rejected because laws are canonical and should change less often than guidance. 2) Hook-level enforcement: rejected because hooks can't validate intent. 3) AGENTS.md hardening: chosen as the developer-facing first line of defense.`
- boundary_non_goals: `No change to LAWS.md §2D. No hook behavior changes. No new enforcement mechanisms.`
- residual_risk: `AGENTS.md is natural-language guidance; AI can still ignore it. Future hook-level improvements may strengthen enforcement.`

## Verification
- AGENTS.md line 114 rewritten from 33 chars to 280 chars
- Lists forbidden patterns explicitly (small change, in a hurry, docs/cleanup)
- Narrows verified_false_negative to "gate's factual assertion contradicts the merge diff"
- Candidate C-20260426-0002-A tracks this as proposed pre-IBM research
