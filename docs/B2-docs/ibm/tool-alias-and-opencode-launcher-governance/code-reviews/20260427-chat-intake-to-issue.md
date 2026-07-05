# Chat→issue migration - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Migrate chat/intake to write docs/B1-docs/raw-{key}/issue.md. Add scan_raw_issues() to task-source-scan.py. Keep .freely/intake/ for backward compat.`
- why_this: `Unifies input sources per IBM Framework B1_IBM design. Chat messages now create raw issues that enter B1 via scan.`
- alternatives_considered: `1) Remove .freely/intake/ immediately: rejected, too risky. 2) Only add scan: rejected, need both write and scan. 3) Dual-write: chosen, safe migration.`
- boundary_non_goals: `No chat-routing skill implementation (AI routing deferred). No .freely/intake/ removal.`
- residual_risk: `Low. Both old and new paths active. Scan picks up both.`
