# Issue-sync dedup and scan-state - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add scan-state (.scan-state file tracking sync timestamps/hashes), dedup checks (create checks platform_ids, update checks content hash, comment checks last_synced_comment_at), batch/scan commands.`
- why_this: `Without dedup, bin/issue-sync would re-create existing platform issues and re-push unchanged content. The .scan-state file enables incremental sync (only changed issues).`
- alternatives_considered: `1) No dedup (current): rejected, spam. 2) Per-issue hash files: rejected, scattered. 3) Single .scan-state JSON: chosen, centralized.`
- boundary_non_goals: `No phase_state backfill for old issues (phase lives in canonical docs).`
- residual_risk: `First run has no baseline hash — all issues appear unchanged until explicitly synced. Resolved by batch seeding on first run.`

## Verification
- bash -n: `pass`
- create dedup: `pass` (skip create: already on GitHub)
- update dedup: `pass` (skip update: unchanged since last sync)
- scan first run: `pass` (shows none — correct initial state)
- macOS sed fix: `pass` (awk replacement for frontmatter stripping)
