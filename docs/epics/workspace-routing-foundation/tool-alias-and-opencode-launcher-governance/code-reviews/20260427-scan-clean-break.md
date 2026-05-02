# Scan clean break - verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Remove scan_intake from build_payload. Add scan_linked_issues for I-* detection. Replace with scan_raw_issues.`
- why_this: `.freely/intake/ is deprecated. All input sources are now docs/issues/ raw and linked issues.`
- alternatives_considered: `1) Keep both scans: rejected, redundant. 2) Only raw issues: rejected, linked issues with new comments need attention too. 3) Full clean break: chosen.`
- boundary_non_goals: `No interruption handler changes in this slice.`
- residual_risk: `Linked issue scan may need tuning for comment resolution state tracking.`
