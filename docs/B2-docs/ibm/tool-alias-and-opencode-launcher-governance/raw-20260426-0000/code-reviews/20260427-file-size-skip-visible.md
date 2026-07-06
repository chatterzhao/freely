# File size skip visibility - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Output [SKIP] for files with skip markers instead of silently ignoring them. Track skip count in summary.`
- why_this: `Silent skips hide information — users can't see which files are excluded. Making skips visible gives a complete picture of the scan.`
- alternatives_considered: `1) Silent skip (current): rejected, incomplete visibility. 2) Verbose skip reason: rejected, over-engineered. 3) [SKIP] prefix + count: chosen, simple and transparent.`
- boundary_non_goals: `No per-file skip reason output. No SKIP level configuration.`
- residual_risk: `Minimal — purely additive change to output format.`

## Verification
- bash -n: `pass`
- execution: `pass` (1 SKIP shown for docs/milestones.md, summary includes Skips: 1)
- skip marker detection: `pass` (grep pattern unchanged, same files detected)
- counter accuracy: `pass` (skips counter matches [SKIP] output lines)
